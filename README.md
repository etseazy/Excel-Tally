# Excel2Tally

A simple, user-friendly tool to transfer transactions from Excel to Tally ERP 9/Prime via Tally's XML API.

---

## Features

- Clean and intuitive 3-step GUI
- Preview transactions before sending to Tally
- Validates Excel data for required columns and empty fields
- Generates Tally-compatible XML
- Sends data directly to Tally via HTTP
- Error handling and helpful status messages

---

## Requirements

### Software Requirements
- Python 3.8+ (if running from source)
- Tally ERP 9 or Tally Prime (with ODBC/HTTP Gateway enabled, usually on port 9000)
- Windows 7/8/10/11

### Excel File Format
Your Excel file MUST have exactly these 4 columns with exact names:

| Column Name  | Description           | Example          |
|--------------|-----------------------|------------------|
| **Date**     | Transaction date      | 10-04-2025       |
| **Amount**   | Transaction amount    | 100 (+ve) or -50 (-ve) |
| **Narration**| Description           | "Fees received"  |
| **GL**       | General Ledger account| "Suspense"       |

**Important Notes:**
- Column names are case-sensitive.
- Positive amounts = Cash receipts (Cash Dr, GL Cr).
- Negative amounts = Cash payments (GL Dr, Cash Cr).

---

## Setup

### Run from Source

1. **Clone or Download the Repository**
   ```bash
   git clone <repository-url>
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure Tally is Running**
   - Open your company in Tally.
   - Make sure the Tally Gateway Server is enabled (default: port 9000).

4. **Prepare Your Excel File**
   - Required columns: `Date`, `Amount`, `Narration`, `GL`
   - Example: See `data.xlsx` for the template.

---

## Usage

### Run from Source

```bash
python main.py
```

### As a Standalone Executable

If you have the `.exe` (e.g., `Excel2Tally.exe`):

1. Double-click the executable, or run from command line:
   ```bash
   Excel2Tally.exe
   ```

---

## How It Works

1. **Select your Excel file**  
   The app checks for required columns and loads your transactions.

2. **Preview your data**  
   See a summary of the transactions to be sent to Tally.

3. **Transfer to Tally**  
   The tool generates XML and sends it to Tally.  
   You’ll get a success or error message, and a preview XML is saved as `tally_preview.xml`.

---

## Troubleshooting

- **Tally not responding?**
  - Make sure Tally is running and the Gateway Server is enabled (port 9000).
  - The company you want to import into must be open in Tally.
  - All ledger names in your Excel must exist in Tally.

- **Ledger does not exist error?**
  - Check that all `GL` values in your Excel match ledger names in Tally exactly.

- **Other issues?**
  - See `Troubleshooting steps.txt` for more help.

---

## Customization

- To change the default company, edit the `<SVCURRENTCOMPANY>` value in `xml_generator.py`.
- To change the icon for the executable, use the `--icon=youricon.ico` option with PyInstaller.

---

## License

This project is provided publicly for educational and personal use only.  
**Not intended for commercial or production use.**

