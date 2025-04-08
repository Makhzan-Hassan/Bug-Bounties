import requests
import re


def sql_injection_test(url):
    """Basic SQL Injection Test"""
    payload = "' OR '1'='1"  # Common SQL Injection payload
    test_url = f"{url}?id={payload}"

    try:
        response = requests.get(test_url)
        if "sql" in response.text.lower() or "database" in response.text.lower():
            print(f"[!] Possible SQL Injection found at: {test_url}")
        else:
            print("[-] No SQL Injection detected.")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")


def xss_test(url):
    """Basic XSS Test"""
    payload = "<script>alert('XSS')</script>"
    test_url = f"{url}?q={payload}"

    try:
        response = requests.get(test_url)
        if payload in response.text:
            print(f"[!] Possible XSS found at: {test_url}")
        else:
            print("[-] No XSS detected.")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")


def weak_authentication_test(url):
    """Check for weak authentication (default passwords)"""
    common_passwords = ["admin", "password", "123456", "admin123"]
    login_url = f"{url}/login"

    try:
        for password in common_passwords:
            response = requests.post(login_url, data={'username': 'admin', 'password': password})
            if "welcome" in response.text.lower():
                print(f"[!] Weak authentication found: admin/{password}")
                return
        print("[-] No weak authentication detected.")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")


def main():
    target_url = input("Enter the target URL: ").strip()

    # Ensure the URL starts with http:// or https://
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        print("[ERROR] Invalid URL format. Make sure to include 'http://' or 'https://'.")
        return

    sql_injection_test(target_url)
    xss_test(target_url)
    weak_authentication_test(target_url)


if __name__ == "__main__":
    main()
