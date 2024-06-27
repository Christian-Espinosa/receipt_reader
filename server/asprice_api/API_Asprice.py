import json, os
import requests

def API_Asprise(image, save_json_file, save_log_file):
    url = "https://ocr.asprise.com/api/v1/receipt"
    
    res = requests.post(url,
        data = {
            'api_key': 'TEST',
            'recognizer': 'auto',
            'ref_no': 'oct_python_123'
        },
        files = {
            'file': open(image, 'rb')
        })

    with open(save_json_file, "w") as f:
        json.dump(json.loads(res.text), f)

    with open(save_json_file, "r") as f:
        data = json.load(f)

    with open(save_log_file, "w") as f:
        f.write(str(data['receipts'][0].keys()) + "\n")

        items = data['receipts'][0]['items']

        f.write(f"Your purchase at {data['receipts'][0]['merchant_name']}\n")

        for item in items:
            f.write(f"{item['description']} - {data['receipts'][0]['currency']} {item['amount']}\n")

        f.write("-" * 30 + "\n")
        f.write(f"Subtotal: {data['receipts'][0]['subtotal']}\n")
        f.write(f"Tax: {data['receipts'][0]['tax']}\n")
        f.write("-" * 30 + "\n")
        f.write(f"Total: {data['receipts'][0]['total']}\n")

    #Print on console
    print(data['receipts'][0].keys())

    print(f"Your purchase at {data['receipts'][0]['merchant_name']}")

    for item in items:
        print(f"{item['description']} - {data['receipts'][0]['currency']} {item['amount']}")

    print("-" * 30)
    print(f"Subtotal: {data['receipts'][0]['subtotal']}")
    print(f"Tax: {data['receipts'][0]['tax']}")
    print("-" * 30)
    print(f"Total: {data['receipts'][0]['total']}")



def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.abspath(os.path.join(current_directory, os.pardir))

    data_dir = os.path.join(server_path, 'input_data')
    save_proc = os.path.join(current_directory, 'response')


    # Iterate through all files in the test_data directory
    for file_name in os.listdir(data_dir):
        if file_name.lower().endswith(('.jpeg', '.jpg', '.png')):
            full_file_path = os.path.join(data_dir, file_name)

            save_file_name = f'result_{file_name}'.rstrip(".jpeg") + '.json'
            save_json_path = os.path.join(save_proc, save_file_name)
            save_file_name = f'log_{file_name}'.rstrip(".jpeg") + '.txt'
            save_log_path = os.path.join(save_proc, save_file_name)
            print(f'=============== OCR {file_name} ===============')
            API_Asprise(full_file_path, save_json_path, save_log_path)

            

if __name__ == '__main__':
    main()
