import requests

API_KEY = "ba3520efa48cddcdecbd28dc2ccf62df755891fa"
url = "https://api.bankfxapi.com/v1/bank/TJNB"
headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(url, headers=headers)

print("Status code:", response.status_code)
print(response.text)  
