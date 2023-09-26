import os
import random
import smtplib
import socks

# ==================
# Load Environment Variable
# ==================
def load_env_variables():
    """
    Load necessary environment variables.
    Returns: Dictionary containing SMTP details.
    """
    return {
        "EMAIL_SUBJECT": os.getenv("EMAIL_SUBJECT", "Test Email from SMTP Checker"),
        "EMAIL_BODY": os.getenv("EMAIL_BODY", "This is a test email sent by the SMTP Checker tool."),
        "RECIPIENT": os.getenv("RECIPIENT", "test@example.com"),
        "USE_PROXIES_HTTP": os.getenv("USE_PROXIES_HTTP", "0"),
        "USE_PROXIES_SOCKS": os.getenv("USE_PROXIES_SOCKS", "0")
    }

# ==================
# Extract SMTP Details
# ==================
def extract_smtp_details_from_sample(line):
    """
    Extract SMTP details from a given line of the sample file.
    Args:
    - line (str): Line from SMTP sample file.
    Returns:
    - Dictionary containing SMTP details or None if the line format is unexpected.
    """
    try:
        details         = line.strip().split(":")
        if len(details) != 4:
            return None
        return {
            "MAILUSER": details[0],
            "MAILPASS": details[1],
            "MAILHOST": details[2],
            "MAILPORT": details[3]
        }
    except Exception as e:
        print(f"Error extracting SMTP details from {line}: {e}")
        return None

# ==================
# Retrieve Random Proxy
# ==================
def get_random_proxy(proxy_type):
    """
    Fetch a random proxy from the respective proxy file.
    Args:
    - proxy_type (str): Type of proxy ("http" or "socks").
    Returns:
    - str: Proxy in format ip:port or None if an error occurred.
    """
    try:
        if proxy_type == "http":
            filename        = "http_proxies.txt"

        elif proxy_type == "socks":
            filename        = "socks.txt"

        else:
            return None

        with open(filename, 'r') as f:
            proxies         = f.readlines()

        if not proxies:
            return None

        return random.choice(proxies).strip()
    except Exception as e:
        print(f"Error fetching random {proxy_type} proxy: {e}")
        return None

# ==================
# Send Test Email
# ==================
def send_test_email(smtp_details):
    """
    Send a test email using the provided SMTP details.
    Args:
    - smtp_details (dict): Dictionary containing SMTP details.
    Returns:
    - bool: True if the email was sent successfully, False otherwise.
    - str: Message indicating the result or the error.
    """
    try:
        # Extracting SMTP details
        SMTP_USER               = smtp_details["MAILUSER"]
        SMTP_PASS               = smtp_details["MAILPASS"]
        SMTP_HOST               = smtp_details["MAILHOST"]
        SMTP_PORT               = int(smtp_details["MAILPORT"])

        # Check if using HTTP proxy
        if os.getenv("USE_PROXIES_HTTP", "0") == "1":
            proxy               = get_random_proxy("http")
            if proxy:
                ip, port        = proxy.split(":")
                socket.setdefaulttimeout(60)
                socket.socket   = socks.socksocket
                socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, ip, int(port))

        # Check if using SOCKS proxy
        if os.getenv("USE_PROXIES_SOCKS", "0") == "1":
            proxy               = get_random_proxy("socks")

            if proxy:
                ip, port        = proxy.split(":")
                socks.set_default_proxy(socks.SOCKS5, ip, int(port))
                socks.wrap_module(smtplib)

        # Email content from environment variables
        EMAIL_SUBJECT           = os.getenv("EMAIL_SUBJECT", "Test Email from SMTP Checker")
        EMAIL_BODY              = os.getenv("EMAIL_BODY", "This is a test email sent by the SMTP Checker tool.")
        RECIPIENT               = os.getenv("RECIPIENT", "test@example.com")

        if SMTP_PORT == 465:
            server              = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        elif SMTP_PORT == 587:
            server              = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
        else:
            raise ValueError(f"Unsupported SMTP port: {SMTP_PORT}")

        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, RECIPIENT, f"Subject: {EMAIL_SUBJECT}\n\n{EMAIL_BODY}")
        server.quit()
        return True, "Success"

    except Exception as e:
        return False, str(e)

