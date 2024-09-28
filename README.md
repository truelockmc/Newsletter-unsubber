# Newsletter Unsubber

The **Newsletter Unsubber** is a simple tool designed to help you quickly and easily unsubscribe from unwanted newsletters. Through a graphical interface, you can securely enter your email credentials, and the tool automatically sends an unsubscribe request to the newsletter provider. Your credentials are stored locally and securely encrypted.

## How It Works

1. **Storing Email Credentials**: On the first launch, you enter your email address, password, and name. These credentials are locally stored in a `credentials.dat` file using strong encryption (Fernet encryption).
2. **Automatic Unsubscribe Email**: Enter the email address of the newsletter provider you wish to unsubscribe from, and the program will send an automatically generated unsubscribe request.
3. **Supports Multiple Email Providers**: The program recognizes common email providers such as Gmail, Yahoo, Outlook, and GMX, and automatically configures the SMTP settings. For unsupported providers, you can manually enter the SMTP server and port.
4. **Easy Data Management**: If you need to update or delete your credentials, this can be easily done through the program.

## Key Features

- **Secure Storage**: Your credentials are encrypted with the Fernet encryption standard and stored locally.
- **Automated Emails**: The software generates and sends an unsubscribe email on your behalf.
- **User-Friendly GUI**: Simple and intuitive graphical user interface (GUI) for managing your email unsubscribe requests.
- **Multiple Email Services**: Supports popular email services such as Gmail, Yahoo, Outlook, GMX, Web.de, and more. Custom SMTP server configuration is also available for unsupported services.
- **One-Click Data Management**: You can easily reset or change your stored email credentials.

## Requirements (For Python Version)

- Python 3.x
- Required Python Libraries:
  - `tkinter`
  - `cryptography`
  - `smtplib`
  - `email`
  - `re`

## Installation and Usage (Python Version)

1. Clone the repository:
    ```bash
    git clone https://github.com/truelockmc/Newsletter-unsubber.git
    cd Newsletter-unsubber
    ```

2. Install dependencies:
    ```bash
    pip install cryptography
    ```

3. Run the program:
    ```bash
    python Newsletter_unsubber.py
    ```

## Using the `.exe` File

If you do not have Python installed or prefer not to run the source code, you can use the precompiled `.exe` file:

1. Download the `Newsletter unsubber.exe` file.
2. Double-click the `.exe` file to launch the program.
3. On the first launch, enter your email credentials (Email, Password, and Name), which are securely stored and only need to be entered once.
4. Enter the email address of the newsletter provider and click "Send Unsubscribe Email" to send the request.
5. If you want to update your saved credentials, click "Change Your Data" and restart the program to enter new credentials.

### Note:
Make sure to run the `.exe` file on a trusted computer since your email credentials will be stored locally. These credentials are, however, protected using strong encryption.

## Supported Email Providers

The following email providers are automatically recognized, and SMTP settings are pre-configured:

- **Gmail**: `smtp.gmail.com`
- **Yahoo**: `smtp.mail.yahoo.com`
- **Outlook/Hotmail**: `smtp.office365.com` / `smtp.live.com`
- **GMX**: `mail.gmx.net`
- **Web.de**: `smtp.web.de`
- **iCloud**: `smtp.mail.me.com`
- **T-Online**: `securesmtp.t-online.de`

For other email providers, you can manually enter the SMTP server and the corresponding port.

## License

This project is licensed under the MIT License.

## Contributing

If you have suggestions for improvements or would like to report a bug, feel free to open an issue or submit a pull request.

---

### Disclaimer
This tool requires your email credentials to send emails. Ensure that you use this tool only on trusted devices to prevent any misuse of your data. However, your credentials are securely encrypted and stored locally.
