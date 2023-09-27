# main.py
import os
from utils import load_env_variables, extract_smtp_details_from_sample, print_banner, print_error, print_success
from leads_management import clean_leads, read_leads_from_file, insert_test_email
from bots import dispatch_leads_to_bots

def main():
    try:
        # Display the banner
        print_banner()

        # Load environment variables
        config              = load_env_variables()

        # Read and clean leads
        leads               = read_leads_from_file(config["LEADS_FILE_PATH"])
        cleaned_leads       = clean_leads(leads)

        # Optionally insert a test email
        if config["INSERT_TEST_EMAIL"] == "1":
            cleaned_leads   = insert_test_email(cleaned_leads, config["TEST_EMAIL_RECIPIENT"], config["INTERVAL_BETWEEN_TEST_EMAIL"])

        # Extract SMTP details
        smtp_details_list   = extract_smtp_details_from_sample(config["SMTPS_FILE_PATH"])  # Update the path accordingly
        #
        # Dispatch leads to bots for concurrent email sending
        dispatch_leads_to_bots(smtp_details_list, cleaned_leads, config["EMAIL_SUBJECT"], config["EMAIL_BODY"], config["BOTS"])

        print_success("Email sending process completed successfully!")

    except Exception as e:
        print_error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
