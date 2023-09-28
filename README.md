# SMTP Checker

This tool is designed to test SMTP server credentials from a sample file and report on their validity.

---

### 📋 **Requirements**:

- **Python Environment**: Ensure you have Python set up on your machine.
- **Python Libraries**: This tool uses the `smtplib` and `os` standard libraries.
- **SMTP Sample File (`smtps.txt`)**: The file should have the following structure:

```
URL: <URL>
METHOD: <METHOD>
MAILHOST: <SMTP_HOST>
MAILPORT: <SMTP_PORT>
MAILUSER: <SMTP_USER>
MAILPASS: <SMTP_PASS>
MAILFROM: <MAIL_FROM> (Optional)
FROMNAME: <FROM_NAME> (Optional)
```

- **Environment Variables**: Store default email subject and recipient in an `.env` file:
- `DEFAULT_EMAIL_SUBJECT`
- `DEFAULT_RECIPIENT`

---

### 🚀 **Plan**:

1. **Load Environment Variables**: Extract values from the `.env` file.
2. **Extract SMTP Details**: Read the `smtps.txt` sample file.
3. **Test SMTP Credentials**:
  - Use provided `MAILFROM` and `FROMNAME` or defaults if not provided.
  - Handle both port 465 (SSL) and ports  [587,585, 1025, 2525, 25] (TLS).
4. **Write Results**:
  - **Success**: Working SMTP credentials are saved to `working_smtps.txt`.
  - **Failure**: Failed SMTP credentials, along with errors, are saved to `failed_smtps.txt`. Both files maintain the structure of the sample file.

---

### 🛠 **Usage**:

1. Ensure the SMTP sample file (`smtps.txt`) is in the same directory as the script.
2. Execute the script: `python main.py`.
3. Review Results:
  - **Valid Credentials**: Check `working_smtps.txt`.
  - **Invalid Credentials**: Refer to `failed_smtps.txt`.
