import pandas as pd
from xml_generator import generate_tally_xml
from tally_sender import send_to_tally


def read_excel(file_path):
    df = pd.read_excel(file_path)
    transactions = df.to_dict(orient='records')
    return transactions

def main():
    # Path to Excel file
    excel_path = "data.xlsx"

    # Read data from Excel
    print("[INFO] Reading Excel file...")
    transactions = read_excel(excel_path)
    print(f"[INFO] Total transactions found: {len(transactions)}")

    if not transactions:
        print("[ERROR] No transactions found in the Excel file.")
        return

    print("[DEBUG] Transactions:", transactions) #debug

    # Generate Tally-compatible XML
    print("[INFO] Generating Tally XML...")
    xml_data = generate_tally_xml(transactions)

    # Optional: Save XML to file for debugging
    # with open("tally_output.xml", "w") as f:
    #     f.write(xml_data)
    # print("[INFO] XML saved to tally_output.xml")

    # Send to Tally
    print("[INFO] Sending data to Tally...")
    success = send_to_tally(xml_data)

    if success:
        print("[SUCCESS] Data successfully sent to Tally.")
    else:
        print("[FAILED] Failed to send data to Tally.")

if __name__ == "__main__":
    main()
