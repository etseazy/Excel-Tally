import requests

TALLY_URL = "http://localhost:9000"  

def send_to_tally(xml_data):
    try:
        headers = {"Content-Type": "application/xml"}
        response = requests.post(TALLY_URL, data=xml_data.encode(), headers=headers)

        if "<LINEERROR>" in response.text:
            error_start = response.text.find("<LINEERROR>") + len("<LINEERROR>")
            error_end = response.text.find("</LINEERROR>")
            error_message = response.text[error_start:error_end]
            print(f"Tally Error: {error_message}")
            return False
        elif "CREATED" in response.text or "ALTERED" in response.text:
            print("Voucher successfully sent to Tally.")
            return True
        else:
            print("Unexpected Tally response:", response.text)
            return False

    except requests.exceptions.RequestException as e:
        print("Error connecting to Tally:", e)
        return False


def save_xml_to_file(xml_data, filename="tally_request.xml"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(xml_data)
    print(f"XML saved to {filename}")
