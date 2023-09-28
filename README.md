# Email Sender Bot

This project provides a solution for sending bulk emails using multiple bots concurrently. It's designed to be flexible, allowing for the use of multiple SMTP servers, and can be configured to use proxies for sending emails.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Files and Modules](#files-and-modules)
- [Contributing](#contributing)
- [License](#license)


## Requirements:

1. Python environment.
2. `smtplib` and `os` Python standard libraries.
3. SMTP sample file (`smtps.txt`) with the following structure:
URL: <URL>
METHOD: <METHOD>
MAILHOST: <SMTP_HOST>
MAILPORT: <SMTP_PORT>
MAILUSER: <SMTP_USER>
MAILPASS: <SMTP_PASS>
MAILFROM: <MAIL_FROM> (Optional)
FROMNAME: <FROM_NAME> (Optional)


## Setup

1. Clone the repository.
2. Install the required dependencies.
3. Set up your `.env` file with the necessary configurations (see [Configuration](#configuration) section).

## Configuration

The `.env` file contains various configurations for the email sender:

- **Email Content**: Set your default email subject and body.
- **Proxy Configuration**: Choose whether to use HTTP or SOCKS proxies.
- **File Management**: Specify the path to your leads file and the smtps file.
- **Bots Configuration**: Set the number of bots and the delay between email sends.
- **Logging Configuration**: Specify the path to the log file.
- **Optional Test Email Insertion**: Decide whether to insert a test email at specified intervals.

For a detailed breakdown of each configuration, refer to the provided `.env` file in the repository.

## Usage

1. Ensure your leads file is populated with the email addresses you want to target.
2. If using proxies, make sure the respective proxy files (`http_proxies.txt` and `socks.txt`) are populated.
3. Ensure your smtps file is populated with the smtps credentials in the right format.
4. Run the `main.py` script to start the email sending process.

## Files and Modules

- **.env**: Contains configuration details.
- **utils.py**: Utility functions for the project.
- **bots.py**: Logic related to the email sending bots.
- **leads_management.py**: Functions related to managing and cleaning email leads.
- **main.py**: The main execution script that organizes and calls other methods.

## Contributing

Contributions are welcome! Please ensure that any changes made are in line with the project's overall goals and functionalities.

## License

This project is licensed under the MIT License.
