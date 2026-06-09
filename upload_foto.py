#!/usr/bin/env python3
"""
Script per scaricare le foto dalla mail Gmail e caricarle su GitHub.
Eseguire localmente con: python3 upload_foto.py

Requisiti: pip install google-auth-httplib2 google-api-python-client requests
"""

import base64
import json
import os

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")  # Imposta: export GITHUB_TOKEN=...
REPO = "euroteamintadv/monteguardia"
BRANCH = "feature/foto-reali-emiliano"

# Mappa: nome_file_destinazione -> attachment_id Gmail (dal msg 19ea191c593ee6ce)
ATTACHMENTS = {
    "sfondo-copertina.jpg": "ANGjdJ9yFZAskvo31VZKaUiOhmfny3hPX3Buku14NjF2ymFBC0Y6TReisn8lm5pV6JBDqJnL6BSBIfxpR_feZV2trweebnMfv9YdnfRvzKeBeMITc5jL2V4iZayLQVyDm_6Bpz1ly8NJbeIc3dWzXfkiO36XL_ezUEaBsasB0OewFuJlggBRBYYNrXzkojMxJ7WjXAqq9zgRNhbjQwdlhRmLWy3TTI3RgULFdWv-klFMSBCRdnDBk9_YmuSLuznSI3d9uTZEX8tYSRQ19uiSLitLIo18oQocN4kJiJ1IiO1L02xvWagtvG2HBw4S658hsSMpi_wdJl7qoXYnx-DVt2nPn4vqUu1VT5LOL_EnV18aFb6--_A47GohgiChXGok2a6SBIWPw0Ig8tPgmE3TTFEI0TnzTzPcBEadUe03hQ",
    "chi-siamo.jpg":         "ANGjdJ9_5bgYHxYiqK5610EjuAVzItzTGFqDyRTRP3f1uFpwg9uahTNYs2WvceIPZjWkI3p24pz53YMlsdlNotf36vey2I1LGJI7Lvs6Kfk6ZFtJV-SfVTlmazkxOsKOfju2_yK2hw48B3sMeBvN87cf7MKg5tBWWDxKyU9CSxEN3yFxJMi8uow30bmYxmdT-NODUV0UuwlqXuOJgim2deOBFjpu2CAdZFbnhphHUYoGCuOrTkodPZEsyf_BJ4tSLXshB24uhkm3fPMKuA1Z4xvxkE4jP9vKc9ssfkAoV9a4ua5ts5Z9O8XcuF4RWgg_Yev2Gsyb-wfISC-l5GGHr8qTuC6FPaocCu_CmblEwaVdSbGCYWi8qVLGIXj37A9EUHdijgnThzPvTzIeGRPGYK7bB66SAQPz9ALTT5VQ-Q",
    "gallery-1.jpg":         "ANGjdJ_SGTqKlCzy_kSHLs8o0hsttck-mHfGXmO-Ar98WjvfMMZvmPFIAGRDGVzVper8xSz2pEdljKwDG34FaRzU_aeZND_tMoTwtpZmnayRgaRi4Ig9SBoIKzVep6R5sW2Y0SKdK3f6Kk1N-5nYTqotnOryXU90Jr45GYQlIKnExG57ZhuRnYoTKiIOrVgzTzODgTcTBxLZ2yg0uxD-xNOO9NeYW2k2cUiwyR6tvCurz1dNKGghjf1gh91mcQgSv1bVLHYWNdqrSNjBtIZu0A-PlKrM6-0BxVAtMxAXWYic5g7eFPhYabtjUZduWvMZIrfUPbmt_mFHCBojds5pzuqd_z1n6VROdqwemL2oIQ_7yug53zAcvg3DdOLRDtnvpnmFPBiMYX4SsxoEEDQC",
    "gallery-2.jpg":         "ANGjdJ93oNcNJUjDyodaeaI8GEXLGKTvDM0RWZXmfai6_LqZMhK-74B_ffycgck4s2MZsr4g6row0xhcjtRvVgSSJTIZwT5xRmKshEhtOCVqk28tpgJrCxqmP1tSVni9qUSEh7wG6cm70SMsps5OW0Re83rN6Qb7y2Xs9CMQd1R-1bjkv0xLgR1BxJsZEriPz2fYyKXYt0PcsOM0V9ar0LTWAmpq0HmghG0K5dE6Mq5GkieQFjMBQSzs7OwdZYZ16sz8da2tb5r5KbP1qgcHw679qI_cIEP6d0PH-o54LZpWAFMKHvsysQQBu7Xpn8uS-LHXVxwMumegNmOsQXPfFPEw8FGTPIuVS1J4iPeeoHYdOWNLqLsx40qCglVuy9FuKbsNul7La8SIQooH2Htw28JMgVJci21menOdz73coA",
    "gallery-3.jpg":         "ANGjdJ8dZj-6X-Yq_kYTEEfKy_hmqhUHuEpBRtD66fZ4gYFSE_iOrmJw-Rz0BV_dzm6cQuAiRlrayp1z3pdxEdgORsYYKGiO4nUeXPcaqjNmaJMIX3xvczENgdPHHyKQnBT_2N8xP0aeHJMoAr_ODFmsQ3NEdswgqzYcXknJ0nI0Nbfmm1WEW2e5ZpJp3okJuVLnpwkfZYlUVOSAYvn65YXFBwnmX3owVvyRH2PMXDnvYrTWgHBzu9j5BOhpR-Hor3DC4ellRSMSvIpfCd9oXFrY597q09RUWesJmLo7c1hElxexRRmmFtbohWbvax0Y7u2LOvUnx_Y9RAq3qy0_sXHwj2REQguBsphaf5hSDOpnBVvp_Etb9FBmR3vUGHU3gb-Ig1653SWpgiG1PTJLD3tetFWrBLsz27JOpQRWkg",
    "gallery-4.jpg":         "ANGjdJ9RrNBmAUJg1uxFkiOyx5akvuxLAS_u4muqK_rVcE0IPPCqIuY97RjVWKunsqKORvoEYvsOWi0xqBtt0oQ_tGKA28qH09t8gPnEzDQRVJpUi3lWXjhSRCq7KGVWPzekOXXEF8HqQtxy5bx5aVUkkxST62B-fBqtqd1TN7diQFulSDRfXA0XtVH4HJR0Tgw77345_7m3YSeUN0cAWaHO3Psa_8oy6fbmi7qiGTWIKFPQOTtd111PdHivg5C-xhGfOELJCarLUJKLqEvUdtrNK4uw39TOPcQQ5ccasIezewlckzVGBThA6jcs7IVLUDmPBSsojdnOqQgooQBYtzvX7B5hqb4ARMyayQS2ifCBGrH3fAzNz4rOTG_ddVmD8Ieo2I_4D0fMRwWICicIQVLVIKb6zM9T-qHeBoIdKw",
    "gallery-5.jpg":         "ANGjdJ9RLzZlS1M35wwdWrevwe7uib-HjDc1qZPwOQFV9nPWtisDEk4PwcygnnYGVx-3SjKbVVnB8fUy5kN85nuJoGh2qgh5XCZxWzpzyvX3em23r9_1dRtT5Cd63vi5CWOdxvyQu4RW3KhXXl8EwxjKOTCn_Fz4e5oI1mX0Wel-MuVZFwN9HR7ESnKyXn9TMGJ762TzQ2T1KXuyVoxHQ3ruM97laF-GA0LJfR1T4UaHeKvjO1xTyHyA0N6E8u_NA0kTr_oOnwWPu7H1paQl7JGZVZHJdL6b3BEyBdfZnh4Y285bY2PMFfjAu1tZYSo1RW1Xq8-59aKDtqAPLS7xbPgnfrFUJQvpdQ22pV25PbyucxwJ_SS2q9UDicjzlr0h6QiH_OdI6ySMUy7kleU5LwbLqBcRD2_yNJ9UcJMsag",
    "gallery-6.jpg":         "ANGjdJ-749bW4tkIVUNuD2bAdLyqhO76dqoFWGa2OUg-u5lDcjncqZEuKYCrvWWIpFD_YQdWzV8Ck2eKITc1L3sXaBTvrQEeDjoU3ZYt03r3P7CJg_UeYIrg6bqwxhuPlSbRH9sFjWxllpYeajUOGiPh1BGNvXi-P75E4DPv6vb6nYzEjSapPPiDITGA-KX0XUeGq8-_quAwQEPoKgyTljqZgK0HXsijg_nhrFKrslBjo5SQC4sjaUf0IOv7pkjOfsopQxQF0Y_1vJ0ixPYHnOnAtaA61kyeFl3DqAGS7byIyIUmzyb1p8PSfqar3f8LbtOLN3Nfo37bOVZKVU_fwLXTPCXcM2ER0l-P9NWaVcoFBmrv0lALbwjypIWBaYEdrlG2fiQf2bgwtPsUOlDk630-x5VF7l65bpw_X8oKRg",
    "spaghetti-vongole.jpg": "ANGjdJ9bgOrL7puMfQHBaYHNRlrM6DxMwLk7dkc-RdlIrqc8Iqv5M6cFHcBDq4CP84VetACmSHwjK1cebfikNhX2LafrA3GSQ6BalQHpMezdZrHya_wgZi40n1Zv9eYZuC_zxv0noUE1a4r3dxSkLOaFcvWSskfxgfSXMTvjZMESOH1M8QpuwXGBxseP9KkCHDr_sOCBkPb410ShaS_BHTXYBmJbpRPf6SiUKp9JqdnKAXYV2Yxvm3z5hX-QDEIorAThN5-FD3vlL77QEsOnkhvJRKlz4LZ4r2BrmuEj_FdXjjAyF3ObNdjhXK5awbw8szUnRjtF09NxiJ5u2Nr9ByagcV7uRvj0qSIf6pIbs4T1fBu3-iCztLUhhKVe_lkKmhoSQMjw-B6Mb7cXLoA0WWeZUPU35eGl4NZIzGSlVg",
    "granseola.jpg":         "ANGjdJ-f0ku6Zsn6X6csLuj5dwzyaTlFT3Oh38V4Y6ViwKohxqhITq0GYYn8p7mj4H9yMBlJ69DTC9-XbhfLLQiCTdTTVP3UBhSLvBj5vzQYlZnsOnjN7P7uJ6dinbmebLi9tz0hgNw5zmtdWAq5Esc_GH1sXbgKuYgSZdcu4ABWwRZTFK6mVJlX3UCf4XxAy6i7AHZDKoGakJFhueCaf-959XJohR3tPVUV5eMMm8daG0m_WL61LNKDHUOmGC7Q-OSpZ38PHKLlRBSA1OQl1SJnQytP0kdulHbyAzf6F9_v-W8WW_juYjkLWNYi3oWAdXKmaTXq3aBMMRP-Bf5dcVWBG1b2ijFh3Mk14cN2LGGt2jgoLrsd4j6ZaxJM4IUeWNLQ8rJG2gvOrQed3cLUxDyBtBiiBe-ORBQ8YKfJaw",
}

MSG_ID = "19ea191c593ee6ce"

def get_gmail_token():
    """Leggi il token OAuth di Gmail — sostituisci con il tuo access token"""
    # Ottieni il token con: gcloud auth print-access-token
    # oppure usa google-auth: credentials.token
    raise NotImplementedError("Inserisci il tuo Gmail OAuth access token")

def download_attachment(gmail_token, msg_id, att_id):
    import urllib.request
    url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}/attachments/{att_id}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {gmail_token}"})
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    # Gmail usa URL-safe base64
    return base64.urlsafe_b64decode(data['data'] + '==')

def upload_to_github(img_bytes, filename, branch):
    import urllib.request
    content_b64 = base64.b64encode(img_bytes).decode('utf-8')
    path = f"images/{filename}"
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    
    # Controlla se il file esiste già
    req = urllib.request.Request(url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    try:
        with urllib.request.urlopen(req) as r:
            existing = json.loads(r.read())
            sha = existing.get('sha')
    except:
        sha = None
    
    payload = {
        "message": f"add: foto reale {filename}",
        "content": content_b64,
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha
    
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method='PUT',
                                  headers={"Authorization": f"token {GITHUB_TOKEN}",
                                           "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

if __name__ == "__main__":
    gmail_token = get_gmail_token()
    for filename, att_id in ATTACHMENTS.items():
        print(f"Downloading {filename}...")
        img = download_attachment(gmail_token, MSG_ID, att_id)
        print(f"  {len(img)} bytes — uploading to GitHub...")
        result = upload_to_github(img, filename, BRANCH)
        print(f"  ✅ {result.get('content', {}).get('path', 'done')}")
    print("\nTutte le foto caricate!")
