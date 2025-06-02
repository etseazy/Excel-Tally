import pandas as pd

def generate_tally_xml(transactions):
    """Generate Tally XML from transactions - no format changes"""
    entries_xml = ""

    for row in transactions:
        # Use date exactly as provided, convert to Tally format
        try:
            date_str = pd.to_datetime(row['Date']).strftime('%Y%m%d')
        except:
            # If date conversion fails, skip this transaction
            print(f"[WARNING] Skipping transaction with invalid date: {row['Date']}")
            continue
            
        amount = float(row['Amount'])
        narration = str(row['Narration'])
        gl = str(row['GL'])

        # Determine Debit/Credit based on amount sign (as per your logic)
        if amount >= 0:
            dr_account = "Cash"
            cr_account = gl
        else:
            dr_account = gl
            cr_account = "Cash"
            amount = abs(amount)

        # Generate Tally XML voucher entry
        entries_xml += f"""
        <TALLYMESSAGE>
            <VOUCHER VCHTYPE="Receipt" ACTION="Create">
                <DATE>{date_str}</DATE>
                <NARRATION>{narration}</NARRATION>
                <VOUCHERTYPENAME>Receipt</VOUCHERTYPENAME>
                <PARTYLEDGERNAME>{cr_account}</PARTYLEDGERNAME>
                <ALLLEDGERENTRIES.LIST>
                    <LEDGERNAME>{dr_account}</LEDGERNAME>
                    <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
                    <AMOUNT>-{amount}</AMOUNT>
                </ALLLEDGERENTRIES.LIST>
                <ALLLEDGERENTRIES.LIST>
                    <LEDGERNAME>{cr_account}</LEDGERNAME>
                    <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
                    <AMOUNT>{amount}</AMOUNT>
                </ALLLEDGERENTRIES.LIST>
            </VOUCHER>
        </TALLYMESSAGE>
        """

    # Wrap in complete Tally XML structure
    full_xml = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>Vouchers</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>$$CURRENTCOMPANY</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                {entries_xml}
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
    
    return full_xml.strip()