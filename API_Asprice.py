import json
import requests

url = "https://ocr.asprise.com/api/v1/receipt"
image = "receipt1.jpeg"

res = requests.post(url,
    data = {
        'api_key': 'TEST',
        'recognizer': 'auto',
        'ref_no': 'oct_python_123'
    },
    files = {
        'file': open(image, 'rb')
    })

with open("response1.json", "w") as f:
    json.dump(json.loads(res.text), f)

with open("response1.json", "r") as f:
    data = json.load(f)

print(data['receipts'][0].keys())

items = data['receipts'][0]['items']

print(f"Your purchase at {data['receipts'][0]['merchant_name']}")

for item in items:
    print(f"{item['description']} - {data['receipts'][0]['currency']} {item['amount']}")

print("-" * 30)
print(f"Subtotal: {data['receipts'][0]['subtotal']}")
print(f"Tax: {data['receipts'][0]['tax']}")
print("-" * 30)
print(f"Total: {data['receipts'][0]['total']}")
