import requests
import random
import json
import re

# --- Browserless API Configuration ---
BROWSERLESS_API_KEY = "2Tn8NhyDBfg4FSH4f10f994e1dca40357fa39e7d5f7314b23"
BROWSERLESS_BASE_URL = "https://production-sfo.browserless.io"

# --- Pre-defined lists for rotating user data ---
first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
email_domains = ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com"]

def get_random_phone_number():
    """Generates a random US-formatted phone number."""
    return f"{random.randint(201, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def process_order_with_browserless():
    """
    Process order using Browserless API with USA residential proxy
    """
    try:
        # Generate random user data
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(10,99)}{random.choice(email_domains)}"
        phone_number = get_random_phone_number()
        
        print("="*70)
        print("BOJANGLES ORDER AUTOMATION (BROWSERLESS + USA PROXY)")
        print("="*70)
        print(f"[*] Using Browserless API with USA Residential Proxy")
        print(f"\n[*] Using Rotated User Data:")
        print(f"    - Name: {first_name} {last_name}")
        print(f"    - Email: {email}")
        print(f"    - Phone: {phone_number}")
        
        # Step 1: Get access token using Browserless Content API
        order_id = "def67214-7132-4e25-a8ea-7a18923f734f"
        token_url = f'https://www.bojangles.com/api/v1/orders/{order_id}/token'
        
        print(f"\n[*] Fetching access token via Browserless Content API...")
        
        # Use Browserless Content API with USA proxy
        content_api_url = f"{BROWSERLESS_BASE_URL}/content?token={BROWSERLESS_API_KEY}&proxy=residential&proxyCountry=us"
        
        response = requests.post(
            content_api_url,
            headers={'Content-Type': 'application/json'},
            json={
                'url': token_url,
                'waitForTimeout': 2000
            },
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"[!] Browserless API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        # Parse the HTML content to extract JSON
        html_content = response.text
        
        # Try to find JSON in the HTML
        json_match = re.search(r'\{[^{}]*"accesstoken"[^{}]*\}', html_content, re.IGNORECASE)
        if json_match:
            token_data = json.loads(json_match.group())
            access_token = token_data.get('accesstoken') or token_data.get('accessToken')
        else:
            # Try to parse the entire content as JSON
            try:
                token_data = json.loads(html_content)
                access_token = token_data.get('accesstoken') or token_data.get('accessToken')
            except:
                print(f"[!] Could not parse token from response")
                print(f"Response preview: {html_content[:500]}")
                return
        
        if not access_token:
            print(f"[!] Access token not found in response")
            return
        
        print(f"[+] Successfully retrieved Access Token: {access_token}")
        
        # Step 2: Submit order using Browserless Unblock API
        print(f"\n[*] Submitting order via Browserless Unblock API...")
        
        submit_url = f'https://www.olocheckout.com/api/baskets/{order_id}/submit'
        
        # Prepare order data
        order_data = {
            'brandAccessId': 'pOsOaQRlbWrRjoMlO82GyeaaXhVRBNwn',
            'accessToken': access_token,
            'firstName': first_name,
            'lastName': last_name,
            'emailAddress': email,
            'contactNumber': phone_number,
            'customData': [],
            'billingAccounts': [{
                'billingFields': [],
                'billingMethod': 'creditcard',
                'expiryYear': '2028',
                'expiryMonth': '10',
                'zip': '10080',
                'saveOnFile': False,
                'amount': 11.49,
                'tipPortion': 0,
                'cardNumber': '4677845104934858',
                'cvv': '548',
            }],
            'bookingUserOptIntoSms': False,
            'createOloAccount': False,
        }
        
        # Use Browserless Unblock API to submit the order
        unblock_api_url = f"{BROWSERLESS_BASE_URL}/unblock?token={BROWSERLESS_API_KEY}&proxy=residential&proxyCountry=us"
        
        submit_response = requests.post(
            unblock_api_url,
            headers={'Content-Type': 'application/json'},
            json={
                'url': submit_url,
                'method': 'POST',
                'headers': {
                    'Content-Type': 'application/json',
                    'x-olo-domain-origin': 'https://www.bojangles.com',
                    'x-olo-request': '1'
                },
                'body': json.dumps(order_data),
                'waitForTimeout': 5000
            },
            timeout=90
        )
        
        # Display results
        print("\n" + "="*70)
        print("FINAL RESPONSE")
        print("="*70)
        print(f"Status Code: {submit_response.status_code}")
        
        response_text = submit_response.text
        print(f"\nResponse Body:")
        print(response_text)
        
        if submit_response.status_code == 200:
            # Check if response contains success indicators
            if 'cloudflare' in response_text.lower() and 'blocked' in response_text.lower():
                print("\n[-] Blocked by Cloudflare despite using Browserless")
            else:
                print("\n[+] Request completed successfully!")
        elif submit_response.status_code == 403:
            print("\n[-] Blocked by Cloudflare (403 Forbidden)")
        else:
            print(f"\n[!] Unexpected status code: {submit_response.status_code}")
        
        print("="*70)
        
    except requests.exceptions.Timeout:
        print("\n[!] Request timed out. Browserless might be taking too long.")
    except requests.exceptions.RequestException as e:
        print(f"\n[!] Network error: {e}")
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    process_order_with_browserless()
