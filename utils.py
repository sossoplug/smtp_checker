import datetime
import os
import random
import smtplib
import socks, socket

# ==================
# Load Environment Variable
# ==================
def load_env_variables():
    """
    Load necessary environment variables.
    Returns: Dictionary containing SMTP details.
    """
    return {
        "EMAIL_SUBJECT":        os.getenv("TEST_EMAIL_SUBJECT"),
        "EMAIL_BODY":           os.getenv("TEST_EMAIL_BODY"),
        "RECIPIENT":            os.getenv("TEST_EMAIL_RECIPIENT"),
        "USE_PROXIES_HTTP":     os.getenv("USE_PROXIES_HTTP", "0"),
        "USE_PROXIES_SOCKS":    os.getenv("USE_PROXIES_SOCKS", "0"),
        "LOG_OUTPUT_FILEPATH":  os.getenv("LOG_OUTPUT_FILEPATH")
    }

# ==================
# Extract SMTP Details
# ==================
def extract_smtp_details_from_sample(file_path):
    """
    Extract SMTP details from a given file.

    Args:
    - file_path (str):                      Path to the file containing SMTP details.

    Returns:
    - list[dict]:                           A list of dictionaries containing SMTP details.
    """
    try:
        smtp_details_list                   = []

        with open(file_path, 'r') as f:

            smtp_details                    = {}
            for line in f:
                if not line.strip():  # Empty line, indicates end of one set of details
                    if smtp_details:
                        smtp_details_list.append(smtp_details)
                        smtp_details        = {}
                    continue

                key, value = line.split(":", 1)
                smtp_details[key.strip()]   = value.strip()

            # Append the last set if it wasn't added due to a missing empty line at the end
            if smtp_details:
                smtp_details_list.append(smtp_details)

        return smtp_details_list

    except Exception as e:
        print(f"Error extracting SMTP details from {file_path}: {e}")
        return []

# ==================
# Retrieve Random Proxy
# ==================
def get_random_proxy(proxy_type):
    """
    Fetch a random proxy from the respective proxy file.
    Args:
    - proxy_type (str):     Type of proxy ("http" or "socks").
    Returns:
    - str:                  Proxy in format ip:port or None if an error occurred.
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
    - smtp_details (dict):      Dictionary containing SMTP details.
    Returns:
    - bool:                     True if the email was sent successfully, False otherwise.
    - str:                      Message indicating the result or the error.
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
        EMAIL_SUBJECT           = os.getenv("TEST_EMAIL_SUBJECT")
        EMAIL_BODY              = os.getenv("TEST_EMAIL_BODY")
        RECIPIENT               = os.getenv("TEST_EMAIL_RECIPIENT")

        if SMTP_PORT == 465:
            server              = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        elif SMTP_PORT in [587, 585, 525, 1025, 2525, 25]:
            server              = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
        else:
            raise ValueError(f"Unsupported SMTP port: {SMTP_PORT}")

        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, RECIPIENT, f"Subject: {EMAIL_SUBJECT}\n\n{EMAIL_BODY}")
        print(f"==================================================")
        print(f"Smtp Check Result: {SMTP_HOST} works")
        write_to_log(f"==================================================", "")
        write_to_log(f"Smtp Check Result: {SMTP_HOST} works", "INFO")
        server.quit()
        return True, "Success"

    except Exception as e:
        print(f"==================================================")
        print(f"Smtp Check Result: {SMTP_HOST} failed - {e}")
        write_to_log(f"==================================================", "")
        write_to_log(f"Smtp Check Result: {SMTP_HOST} failed - {e}", "INFO")
        return False, str(e)




# ===================
#  Wipe Clean a file
# ===================
def wipe_file_clean(file_path):
    """
    Wipe clean a file
    - file_path (str):   Path to the file containing SMTP details.
    Returns:             None.
    """
    try:
        with open(file_path, 'w') as file:
            pass

        print(f"File '{file_path}' has been wiped clean.")

    except Exception as e:
        print(f"An error occurred while wiping the file '{file_path}': {e}")


# ==================
# Write to Log
# ==================
def write_to_log(message, status):
    """
    Write a message to the log file.

    Args:
    - message (str):                    The message to be logged.
    - status (str):                     The status of the message (ERROR/SUCCESS).

    Returns:
    - None
    """
    try:
        timestamp                       = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(os.getenv("LOG_OUTPUT_FILEPATH"), "a") as log_file:
            log_file.write(f"[{timestamp}] INFO: [{status}]: {message}\n")
    except Exception as e:
        print(f"[ERROR]: Failed to write to log. {str(e)}")