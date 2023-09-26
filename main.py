import os
from dotenv import load_dotenv, find_dotenv
from utils import extract_smtp_details_from_sample, send_test_email

# Load environment variables
load_dotenv(find_dotenv())

# File Names
SMTP_SAMPLE_FILE                = "smtps.txt"
WORKING_SMTP_FILE               = "working_smtps.txt"
FAILED_SMTP_FILE                = "failed_smtps.txt"

def main():
    """
    Main function to execute the SMTP testing process.
    """
    try:
        # SMTP Testing
        smtp_details_list       = extract_smtp_details_from_sample(SMTP_SAMPLE_FILE)

        for smtp_details in smtp_details_list:
            success, message    = send_test_email(smtp_details)
            smtp_format         = f"URL: {smtp_details.get('URL', 'N/A')}\nMETHOD: {smtp_details.get('METHOD', 'N/A')}\nMAILHOST: {smtp_details['MAILHOST']}\nMAILPORT: {smtp_details['MAILPORT']}\nMAILUSER: {smtp_details['MAILUSER']}\nMAILPASS: {smtp_details['MAILPASS']}\nMAILFROM: {smtp_details.get('MAILFROM', 'N/A')}\nFROMNAME: {smtp_details.get('FROMNAME', 'N/A')}\n\n"

            with open(WORKING_SMTP_FILE if success else FAILED_SMTP_FILE, 'a') as file:
                file.write(smtp_format)
                if not success:
                    file.write(f"ERROR: {message}\n")

        print("SMTP testing completed.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
