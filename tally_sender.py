import requests
import time

TALLY_URL = "http://localhost:9000"

def send_to_tally(xml_data):
    """Send XML data to Tally with better error handling"""
    try:
        print("Connecting to Tally...")
        
        headers = {
            "Content-Type": "application/xml",
            "Accept": "application/xml"
        }
        
        # Send request to Tally
        response = requests.post(
            TALLY_URL, 
            data=xml_data.encode('utf-8'), 
            headers=headers,
            timeout=30
        )
        
        print(f"Tally Response Status: {response.status_code}")
        
        # Check response content
        response_text = response.text
        
        # Check for Tally errors
        if "<LINEERROR>" in response_text:
            error_start = response_text.find("<LINEERROR>") + len("<LINEERROR>")
            error_end = response_text.find("</LINEERROR>")
            if error_end > error_start:
                error_message = response_text[error_start:error_end]
                print(f"[TALLY ERROR] {error_message}")
            else:
                print("[TALLY ERROR] Unknown line error occurred")
            return False
            
        # Check for success indicators
        elif any(keyword in response_text for keyword in ["CREATED", "ALTERED", "SUCCESS"]):
            print("[SUCCESS] Vouchers accepted by Tally")
            return True
            
        # Check if response is empty (sometimes indicates success)
        elif response.status_code == 200 and len(response_text.strip()) == 0:
            print("[SUCCESS] Data sent successfully (empty response)")
            return True
            
        else:
            print(f"[WARNING] Unexpected Tally response:")
            print(f"Response: {response_text[:200]}...")
            # Still return True if status is 200, as Tally might have accepted it
            return response.status_code == 200

    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to Tally.")
        print("Please ensure:")
        print("1. Tally is running")
        print("2. Gateway is enabled in Tally")
        print("3. Port 9000 is accessible")
        return False
        
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out. Tally might be busy.")
        return False
        
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

def test_tally_connection():
    """Test if Tally is accessible"""
    try:
        response = requests.get(TALLY_URL, timeout=5)
        return True
    except:
        return False