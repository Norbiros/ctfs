import base64
import struct
import requests
import jwt
from randcrack import RandCrack

URL = 'https://easymfa.ecsc25.hack.cert.pl'

predictor = RandCrack()
outputs = []
previous_token = None

for _ in range(312):
    headers = {}
    if previous_token:
        headers['Authorization'] = f'Bearer {previous_token}'
    r = requests.get(f'{URL}/generate', headers=headers).json()
    token = r['token']
    parsed = jwt.decode(token, options={"verify_signature": False})
    print(parsed)
    previous_token = token  # save token for next request
    pwd = base64.b64decode(r['password'])
    print(pwd)
    hi, lo = struct.unpack('>II', pwd)
    predictor.submit(lo)
    predictor.submit(hi)

predictor.offset(-312 * 2)  # go back to the start of the sequence
predictor.offset(-8) #

secret_int = predictor.predict_getrandbits(32 * 8)
secret = secret_int.to_bytes(32, 'big')
admin_token = jwt.encode({'sub': 'admin'}, secret, algorithm='HS256')
print(admin_token)
headers = {'Authorization': f'Bearer {admin_token}'}
resp = requests.post(f'{URL}/flag', json={'OTP': 'kotek'}, headers=headers)

print(resp.text)
