import base64
import re
import struct
import requests
import jwt
from randcrack import RandCrack

URL = 'https://easymfa.ecsc25.hack.cert.pl'


predictor = RandCrack()


headers = {'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiJ9.T02GgnWIEUS1ASYf7wVE-0PXI9C0idUwmuSdvi6dGrk'}

def get_otp():
    resp = requests.post(f'{URL}/flag', json={'OTP': 'kotek'}, headers=headers)
    m = re.search(r'[A-Za-z0-9+/=]{12,}', resp.text)

    if not m:
        print("No OTP found in the response.")
        print(resp.text)
        return

    return base64.b64decode(m.group(0))

for _ in range(312):
    pwd = get_otp()
    hi, lo = struct.unpack('>II', pwd)
    predictor.submit(lo)
    predictor.submit(hi)
    print(pwd)

secret_int = predictor.predict_getrandbits(8 * 8).to_bytes(8, 'big')
b64 = base64.b64encode(secret_int).decode()
print(b64)

headers = {'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiJ9.T02GgnWIEUS1ASYf7wVE-0PXI9C0idUwmuSdvi6dGrk'}
resp = requests.post(f'{URL}/flag', json={'OTP': b64}, headers=headers)


print(resp.text)