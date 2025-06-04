import pandas as pd
import html  # Required to escape XML special characters

def generate_tally_xml(transactions):
    """Generate Tally XML from transactions - escaping special characters"""
    entries_xml = ""

    for row in transactions:
        try:
            date_str = pd.to_datetime(row['Date']).strftime('%Y%m%d')
        except:
            # If date conversion fails, skip this transaction
            print(f"[WARNING] Skipping transaction with invalid date: {row['Date']}")
            continue

        amount = float(row['Amount'])

        # Escape all user-input text fields
        narration = html.escape(str(row['Narration']))
        gl = html.escape(str(row['GL']))

        # Determine voucher type and accounting entries based on amount sign
        if amount >= 0:
            # Positive amount = Money coming IN = Receipt voucher
            voucher_type = "Receipt"
            dr_account = html.escape("Cash")  # Cash debited
            cr_account = gl                   # GL account credited
        else:
            # Negative amount = Money going OUT = Payment voucher
            voucher_type = "Payment"
            dr_account = gl                   # GL account debited
            cr_account = html.escape("Cash")  # Cash credited

        # Generate Tally XML voucher entry
        entries_xml += f"""
        <TALLYMESSAGE>
            <VOUCHER VCHTYPE="{voucher_type}" ACTION="Create">
                <DATE>{date_str}</DATE>
                <NARRATION>{narration}</NARRATION>
                <VOUCHERTYPENAME>{voucher_type}</VOUCHERTYPENAME>
                <ALLLEDGERENTRIES.LIST>
                    <LEDGERNAME>{dr_account}</LEDGERNAME>
                    <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
                    <AMOUNT>-{abs(amount)}</AMOUNT>
                </ALLLEDGERENTRIES.LIST>
                <ALLLEDGERENTRIES.LIST>
                    <LEDGERNAME>{cr_account}</LEDGERNAME>
                    <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
                    <AMOUNT>{abs(amount)}</AMOUNT>
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

