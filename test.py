import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json

r = requests.get("https://apiforproject.herokuapp.com/api/UserProfile/")

print(r.status_code)
print('----------------')
print(r.text)
print('----------------')