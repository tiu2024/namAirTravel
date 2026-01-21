from django.test import Client
from django.contrib.auth import get_user_model
from agency.models import Sale
import re

User = get_user_model()

def run():
    print("Verifying features via HTML content...")
    
    # Setup User
    username = 'verify_admin'
    password = 'password123'
    user, _ = User.objects.get_or_create(username=username, defaults={'role': 'SUPER_ADMIN'})
    user.set_password(password)
    user.save()
    
    client = Client()
    client.force_login(user)

    try:
        response = client.get('/agency/sales/', HTTP_HOST='127.0.0.1')
        if response.status_code == 404:
             response = client.get('/sales/', HTTP_HOST='127.0.0.1')
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return

    print(f"Status Code: {response.status_code}")
    
    if response.status_code != 200:
        print("Failed to access page")
        return

    content = response.content.decode('utf-8')
    
    # 1. Pagination Verification
    # Look for page=2 link or pagination nav
    if '?page=2' in content or 'aria-label="Pagination"' in content:
        print("PASS: Pagination controls found")
    else:
        print(f"FAIL: Pagination controls missing. Length of content: {len(content)}")
        
    # 2. Total Profit Verification
    if 'Total Profit (UZS)' in content and 'Total Profit (USD)' in content:
        print("PASS: Profit Cards present")
        if 'flex justify-end mt-4 gap-4' in content:
             print("PASS: Profit Cards side-by-side (gap-4 present)")
        else:
             print("WARN: Side-by-side classes missing or different")
    else:
        print("FAIL: Profit Cards missing")

    # 3. Salesman Column Verification
    if '>Salesman' in content: # simplistic check for table header
        print("PASS: Salesman column header present")
    else:
        print("FAIL: Salesman column header missing")
        
    if '>Salesman' in content and 'verify_admin' in content: 
         # It might not be 'verify_admin' who made sales, but the column should exist. 
         # The generate_sales script used 'test_salesman'
         if 'test_salesman' in content:
             print("PASS: Salesman data visible")
         else:
             print("WARN: Salesman data verification inconclusive (test_salesman not found)")

if __name__ == '__main__':
    run()
