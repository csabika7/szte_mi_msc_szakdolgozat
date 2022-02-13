import urllib3
import json
import random
import base64

# random noise as test image
raw_img = []
for i in range(0, 28 * 28):
    raw_img.append(random.randint(0, 255))

b64_encoded_img = base64.b64encode(bytes(raw_img))
http = urllib3.PoolManager()
resp = http.request("POST", "http://localhost:5000/v1/model/predict",
                    headers={"Content-Type": "text/plain;base64"},
                    body=b64_encoded_img)
print(resp.status)
print(json.loads(resp.data.decode('utf-8')))
