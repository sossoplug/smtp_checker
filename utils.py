import smtplib
import os


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
