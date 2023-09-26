import os
import smtplib

# ==================
# Set Environment for Proxy
# ==================
def set_environment_for_proxy():
    """
    Set the HTTP_PROXY and HTTPS_PROXY environment variables if proxies or SOCKS are to be used.
    """
    try:
        if os.getenv("USE_PROXIES_HTTP", "0") == "1":
            with open("http_proxies.txt", "r") as file:
                proxy = file.readline().strip()
                os.environ["HTTP_PROXY"] = f"http://{proxy}"
                os.environ["HTTPS_PROXY"] = f"http://{proxy}"
        elif os.getenv("USE_PROXIES_SOCKS", "0") == "1":
            with open("socks.txt", "r") as file:
                sock = file.readline().strip()
                os.environ["HTTP_PROXY"] = f"socks5://{sock}"
                os.environ["HTTPS_PROXY"] = f"socks5://{sock}"
    except Exception as e:
        print(f"Error setting up proxy/socks environment: {e}")

# ==================
# Extract SMTP Details
# ==================
def extract_smtp_details_from_sample(filename):
    """
    Extract SMTP details from the sample file.

    Args:
    - filename (str): The name of the sample file.

    Returns:
    - list: List of dictionaries containing SMTP details.
    """
    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        smtp_details_list = []
        smtp_details = {}
        for line in lines:
            if line.strip() == "":
                if smtp_details:
                    smtp_details_list.append(smtp_details)
                    smtp_details = {}
            else:
                key, value = line.split(": ", 1)
                smtp_details[key] = value.strip()
        if smtp_details:  # For the last set of details
            smtp_details_list.append(smtp_details)

        return smtp_details_list

    except Exception as e:
        print(f"Error extracting SMTP details from {filename}: {e}")
        return []

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
        SMTP_USER = smtp_details["MAILUSER"]
        SMTP_PASS = smtp_details["MAILPASS"]
        SMTP_HOST = smtp_details["MAILHOST"]
        SMTP_PORT = int(smtp_details["MAILPORT"])

        # Email content from environment variables
        EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT", "Test Email from SMTP Checker")
        EMAIL_BODY = os.getenv("EMAIL_BODY", "This is a test email sent by the SMTP Checker tool.")
        RECIPIENT = os.getenv("RECIPIENT", "test@example.com")

        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        elif SMTP_PORT == 587:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
        else:
            raise ValueError(f"Unsupported SMTP port: {SMTP_PORT}")

        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, RECIPIENT, f"Subject: {EMAIL_SUBJECT}\n\n{EMAIL_BODY}")
        server.quit()
        return True, "Success"

    except Exception as e:
        return False, str(e)
