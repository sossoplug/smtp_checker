# bots.py
import threading
import os
from utils import send_bulk_email, print_error

class EmailBot(threading.Thread):
    """
    EmailBot class that extends threading.Thread to send emails concurrently.
    """
    def __init__(self, bot_id, smtp_details, leads_chunk, subject, body):
        threading.Thread.__init__(self)
        self.bot_id         = bot_id
        self.smtp_details   = smtp_details
        self.leads_chunk    = leads_chunk
        self.subject        = subject
        self.body           = body

    def run(self):
        """
        Overridden method from threading.Thread to execute the email sending logic.
        """
        try:
            print(f"Bot-{self.bot_id} started.")
            send_bulk_email(self.smtp_details, self.leads_chunk, self.subject, self.body)
            print(f"Bot-{self.bot_id} completed.")
        except Exception as e:
            print_error(f"Bot-{self.bot_id} encountered an error: {e}")




def dispatch_leads_to_bots(smtp_details_list, leads, subject, body, bots_count):
    """
    Dispatch leads to multiple bots for concurrent email sending.

    Args:
    - smtp_details_list (list[dict]):   List of dictionaries containing SMTP details.
    - leads (list[str]):                Path to the file containing email leads.
    - subject (str):                    Email subject.
    - body (str):                       Email body content.
    - bots_count (int):                 Number of bots to dispatch.

    Returns:
    - None
    """
    try:

        leads_per_bot   = len(leads) // bots_count
        bots            = []

        for i in range(bots_count):
            start_index = i * leads_per_bot
            end_index   = (i + 1) * leads_per_bot if i != bots_count - 1 else None
            bot         = EmailBot(i+1, smtp_details_list[i % len(smtp_details_list)], leads[start_index:end_index], subject, body)
            bots.append(bot)
            bot.start()

        for bot in bots:
            bot.join()

    except Exception as e:
        print_error(f"Error dispatching leads to bots: {e}")
