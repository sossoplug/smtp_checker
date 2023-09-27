# utils.py
import os
import random
import smtplib
import socks, socket
from dotenv import load_dotenv


# ==================
# Load Environment Variables
# ==================
def load_env_variables():
    """
    Load necessary environment variables.

    Returns:
        dict: Dictionary containing configuration details.
    """
    try:
        # Load environment variables from .env file
        load_dotenv()

        return {
            "EMAIL_SUBJECT":                os.getenv("EMAIL_SUBJECT"),
            "EMAIL_BODY":                   os.getenv("EMAIL_BODY"),
            "TEST_EMAIL_RECIPIENT":         os.getenv("TEST_EMAIL_RECIPIENT"),
            "USE_PROXIES_HTTP":             os.getenv("USE_PROXIES_HTTP", "0"),
            "USE_PROXIES_SOCKS":            os.getenv("USE_PROXIES_SOCKS", "0"),
            "SMTPS_FILE_PATH":              os.getenv("SMTPS_FILE_PATH"),
            "CLEANED_LEADS_FILE_PATH":      os.getenv("CLEANED_LEADS_FILE_PATH"),
            "BOTS":                         int(os.getenv("BOTS", 5)),
            "DELAY_IN_SECONDS":             int(os.getenv("DELAY_IN_SECONDS", 1)),
            "LOG_FILE_PATH":                os.getenv("LOG_FILE_PATH"),
            "INSERT_TEST_EMAIL":            os.getenv("INSERT_TEST_EMAIL", "0"),
            "INTERVAL_BETWEEN_TEST_EMAIL":  int(os.getenv("INTERVAL_BETWEEN_TEST_EMAIL", 1000))
        }
    except Exception as e:
        print_error(f"Error loading environment variables: {e}")
        return {}


# ==================
# Banners and Colors
# ==================

def print_banner():
    """
    Display the banner at the start of the script.
    """
    banner = """
    +--------------------------------+
    |                                |
    |       EMAIL SENDER BOT         |
    |                                |
    +--------------------------------+
    """
    print_colored(banner, 'cyan')


def print_colored(message, color):
    """
    Print a colored message to the console.

    Args:
    - message (str): The message to print.
    - color (str): The color to use (e.g., 'red', 'green', 'cyan').
    """
    color_codes = {
        'red': '\033[91m',
        'green': '\033[92m',
        'cyan': '\033[96m',
        'end': '\033[0m'
    }

    print(f"{color_codes[color]}{message}{color_codes['end']}")


def print_error(message):
    """
    Print an error message in red.

    Args:
    - message (str): The error message to print.
    """
    print_colored(f"[ERROR] {message}", 'red')


def print_success(message):
    """
    Print a success message in green.

    Args:
    - message (str): The success message to print.
    """
    print_colored(f"[SUCCESS] {message}", 'green')
# ==================
# Banners and Colors END
# ==================



# ==================
# Extract SMTP Details
# ==================
def extract_smtp_details_from_sample(file_path):
    """
    Extract SMTP details from a given file.

    Args:
    - file_path (str): Path to the file containing SMTP details.

    Returns:
    - list[dict]: A list of dictionaries containing SMTP details.
    """
    try:
        smtp_details_list = []

        with open(file_path, 'r') as f:
            smtp_details = {}
            for line in f:
                if not line.strip():  # Empty line, indicates end of one set of details
                    if smtp_details:
                        smtp_details_list.append(smtp_details)
                        smtp_details = {}
                    continue

                key, value = line.split(":", 1)
                smtp_details[key.strip()] = value.strip()

            # Append the last set if it wasn't added due to a missing empty line at the end
            if smtp_details:
                smtp_details_list.append(smtp_details)

        return smtp_details_list

    except Exception as e:
        print_error(f"Error extracting SMTP details from {file_path}: {e}")
        return []


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
            filename = "http_proxies.txt"
        elif proxy_type == "socks":
            filename = "socks.txt"
        else:
            return None

        with open(filename, 'r') as f:
            proxies = f.readlines()

        if not proxies:
            return None

        return random.choice(proxies).strip()

    except Exception as e:
        print_error(f"Error fetching random {proxy_type} proxy: {e}")
        return None

# ... [More functions will be added as we proceed based on the Detailed Plan]

# ==================
# Leads Management
# ==================
def read_leads_from_file(file_path):
    """
    Read email leads from a given file.

    Args:
    - file_path (str): Path to the file containing email leads.

    Returns:
    - list[str]: A list of email addresses.
    """
    try:
        with open(file_path, 'r') as f:
            return [email.strip() for email in f.readlines() if email.strip()]
    except Exception as e:
        print_error(f"Error reading leads from {file_path}: {e}")
        return []


# ==================
# Send Bulk Email
# ==================
def send_bulk_email(smtp_details, recipient_list, subject, body):
    """
    Send a bulk email using the provided SMTP details to a list of recipients.

    Args:
    - smtp_details (dict): Dictionary containing SMTP details.
    - recipient_list (list[str]): List of email addresses to send to.
    - subject (str): Email subject.
    - body (str): Email body content.

    Returns:
    - bool: True if the emails were sent successfully, False otherwise.
    """
    try:
        # Extracting SMTP details
        SMTP_USER = smtp_details["MAILUSER"]
        SMTP_PASS = smtp_details["MAILPASS"]
        SMTP_HOST = smtp_details["MAILHOST"]
        SMTP_PORT = int(smtp_details["MAILPORT"])

        # Check if using HTTP proxy
        if os.getenv("USE_PROXIES_HTTP", "0") == "1":
            proxy = get_random_proxy("http")
            if proxy:
                ip, port = proxy.split(":")
                socket.setdefaulttimeout(60)
                socket.socket = socks.socksocket
                socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, ip, int(port))

        # Check if using SOCKS proxy
        if os.getenv("USE_PROXIES_SOCKS", "0") == "1":
            proxy = get_random_proxy("socks")
            if proxy:
                ip, port = proxy.split(":")
                socks.set_default_proxy(socks.SOCKS5, ip, int(port))
                socks.wrap_module(smtplib)

        # Email sending logic
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        elif SMTP_PORT == 587:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
        else:
            raise ValueError(f"Unsupported SMTP port: {SMTP_PORT}")

        server.login(SMTP_USER, SMTP_PASS)
        for recipient in recipient_list:
            server.sendmail(SMTP_USER, recipient, f"Subject: {subject}\n\n{body}")

        server.quit()
        return True
    except Exception as e:
        print_error(f"Error sending bulk email: {e}")
        return False
