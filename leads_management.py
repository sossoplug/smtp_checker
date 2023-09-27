# leads_management.py

def clean_leads(leads):
    """
    Clean the leads by removing duplicates and invalid entries.

    Args:
    - leads (list[str]): List of email addresses.

    Returns:
    - list[str]: Cleaned list of email addresses.
    """
    try:
        cleaned_leads = list(set(leads))  # Remove duplicates
        cleaned_leads = [email.strip() for email in cleaned_leads if '@' in email]  # Remove invalid emails
        return cleaned_leads
    except Exception as e:
        print(f"Error cleaning leads: {e}")
        return []


def read_leads_from_file(file_path):
    """
    Read leads (email addresses) from a file.

    Args:
    - file_path (str):  Path to the file containing email leads.

    Returns:
    - list[str]:        List of email addresses.
    """
    try:
        with open(file_path, 'r') as file:
            leads       = file.readlines()

        return [lead.strip() for lead in leads]
    except Exception as e:
        print(f"Error reading leads from {file_path}: {e}")
        return []


def insert_test_email(leads, test_email, interval):
    """
    Insert a test email at specified intervals in the list of leads.

    Args:
    - leads (list[str]): List of email addresses.
    - test_email (str): Test email address to be inserted.
    - interval (int): Interval at which the test email will be inserted.

    Returns:
    - list[str]: List of email addresses with the test email inserted at specified intervals.
    """
    try:
        # Insert test email at the beginning of the list
        leads.insert(0, test_email)

        # Insert test email at specified intervals, starting from the interval index
        for i in range(interval, len(leads), interval):
            leads.insert(i, test_email)

        # Insert test email at the end of the list
        leads.append(test_email)

        return leads
    except Exception as e:
        print(f"Error inserting test email: {e}")
        return leads