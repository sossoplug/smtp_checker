import os
from utils import extract_smtp_details_from_sample, send_test_email

# File Names
SMTP_SAMPLE_FILE    = "smtps.txt"
WORKING_SMTP_FILE   = "working_smtps.txt"
FAILED_SMTP_FILE    = "failed_smtps.txt"


def main():
    """
    Main function to test SMTP configurations and log the results.
    """
    try:
        # Extract SMTP details
        smtp_details_list = extract_smtp_details_from_sample(SMTP_SAMPLE_FILE)

        if not smtp_details_list:
            print(f"No SMTP details found in {SMTP_SAMPLE_FILE}.")
            return

        # Open output files for logging
        with open(WORKING_SMTP_FILE, 'w') as working_file, open(FAILED_SMTP_FILE, 'w') as failed_file:
            for smtp_details in smtp_details_list:
                success, message = send_test_email(smtp_details)

                # Formatting the output
                output_format = "\n".join([f"{key}: {value}" for key, value in smtp_details.items()])

                if success:
                    working_file.write(output_format + "\n\n")
                else:
                    failed_file.write(output_format + f"\nERROR: {message}\n\n")

        print("SMTP testing completed.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
