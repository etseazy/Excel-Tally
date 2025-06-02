import pandas as pd

def generate_tally_xml(transactions):
    entries_xml = ""

    for row in transactions:
        date_str = pd.to_datetime(row['Date']).strftime('%Y%m%d')
        amount = float(row['Amount'])
        narration = row['Narration']
        gl = row['GL']

        # Determine Debit/Credit based on sign
        if amount >= 0:
            dr_account = "Cash"
            cr_account = gl
        else:
            dr_account = gl
            cr_account = "Cash"
            amount = abs(amount)

        # Tally XML entry for one voucher
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

    # Wrap all vouchers into full Tally XML
    full_xml = f"""
    <ENVELOPE>
        <HEADER>
            <TALLYREQUEST>Import Data</TALLYREQUEST>
        </HEADER>
        <BODY>
            <IMPORTDATA>
                <REQUESTDESC>
                    <REPORTNAME>Vouchers</REPORTNAME>
                    <STATICVARIABLES>
                        <SVCURRENTCOMPANY>Open RN</SVCURRENTCOMPANY>
                    </STATICVARIABLES>
                </REQUESTDESC>
                <REQUESTDATA>
                    {entries_xml}
                </REQUESTDATA>
            </IMPORTDATA>
        </BODY>
    </ENVELOPE>
    """
    return full_xml.strip()
