import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import os
import smtplib
from email.mime.text import MIMEText
import re

# Funktion zum Generieren und Speichern eines Schlüssels
def generate_key():
    return Fernet.generate_key()

# Funktion zum Speichern von Zugangsdaten
def save_credentials(email, password, name):
    key = generate_key()
    cipher = Fernet(key)
    encrypted_email = cipher.encrypt(email.encode())
    encrypted_password = cipher.encrypt(password.encode())
    encrypted_name = cipher.encrypt(name.encode())

    with open('credentials.dat', 'wb') as f:
        f.write(key + b'\n' + encrypted_email + b'\n' + encrypted_password + b'\n' + encrypted_name)

# Funktion zum Laden von Zugangsdaten
def load_credentials():
    with open('credentials.dat', 'rb') as f:
        key = f.readline().strip()
        encrypted_email = f.readline().strip()
        encrypted_password = f.readline().strip()
        encrypted_name = f.readline().strip()

    cipher = Fernet(key)
    email = cipher.decrypt(encrypted_email).decode()
    password = cipher.decrypt(encrypted_password).decode()
    name = cipher.decrypt(encrypted_name).decode()
    return email, password, name

# GUI für die Eingabe von E-Mail, Passwort und Name beim Start
def setup_credentials_gui():
    def save_and_close():
        email = email_entry.get()
        password = password_entry.get()
        name = name_entry.get()

        if not email or not password or not name:
            messagebox.showerror("Error", "Please fill out all fields.")
            return
        
        save_credentials(email, password, name)
        setup_window.destroy()
        create_gui()  # Haupt-GUI öffnen, wenn die Daten gespeichert wurden

    setup_window = tk.Tk()
    setup_window.title("Setup Credentials")
    setup_window.configure(bg="#2E2E2E")

    email_label = tk.Label(setup_window, text="Email:", bg="#2E2E2E", fg="white")
    email_label.pack(pady=5)
    email_entry = tk.Entry(setup_window, bg="#4E4E4E", fg="white")
    email_entry.pack(pady=5)

    password_label = tk.Label(setup_window, text="Password:", bg="#2E2E2E", fg="white")
    password_label.pack(pady=5)
    password_entry = tk.Entry(setup_window, show='*', bg="#4E4E4E", fg="white")
    password_entry.pack(pady=5)

    name_label = tk.Label(setup_window, text="Your Name:", bg="#2E2E2E", fg="white")
    name_label.pack(pady=5)
    name_entry = tk.Entry(setup_window, bg="#4E4E4E", fg="white")
    name_entry.pack(pady=5)

    save_button = tk.Button(setup_window, text="Save", command=save_and_close, bg="#4E4E4E", fg="white")
    save_button.pack(pady=20)

    setup_window.mainloop()

# Funktion zum Senden der E-Mail
def send_email():
    try:
        email, password, name = load_credentials()
        provider = provider_entry.get()

        subject = "Unsubscribe from Your Newsletter / Abmeldung von Ihrem Newsletter"
        body = f"""Dear {provider},\n\nI would like to unsubscribe from your newsletter. 
Please remove my email address {email} from your mailing list.\n\n
I kindly request a confirmation of my unsubscription.\n\n
Thank you for your assistance.\n\n
Best regards,\n{name}"""

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = email
        msg['To'] = provider

        smtp_server, smtp_port = get_smtp_info(email)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email, password)
            server.sendmail(email, provider, msg.as_string())

        messagebox.showinfo("Success", "Email sent successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Funktion zum Ermitteln des SMTP-Servers
def get_smtp_info(email):
    if re.match(r".*@gmail\.com", email):
        return "smtp.gmail.com", 587
    elif re.match(r".*@yahoo\.com", email):
        return "smtp.mail.yahoo.com", 587
    elif re.match(r".*@outlook\.com", email):
        return "smtp.office365.com", 587
    elif re.match(r".*@hotmail\.com", email):
        return "smtp.live.com", 587
    elif re.match(r".*@aol\.com", email):
        return "smtp.aol.com", 587
    elif re.match(r".*@t-online\.de", email):
        return "securesmtp.t-online.de", 587
    elif re.match(r".*@web\.de", email):
        return "smtp.web.de", 587
    elif re.match(r".*@gmx\.de", email) or re.match(r".*@gmx\.com", email):
        return "mail.gmx.net", 587
    elif re.match(r".*@icloud\.com", email):
        return "smtp.mail.me.com", 587
    else:
        smtp_server = input("Please enter your SMTP server (e.g., smtp.yourprovider.com): ")
        smtp_port = input("Please enter the SMTP port (usually 587 for TLS): ")
        if not smtp_server or not smtp_port:
            raise ValueError("SMTP server and port are required for unsupported providers.")
        return smtp_server, int(smtp_port)

# Haupt-GUI erstellen
def create_gui():
    root = tk.Tk()
    root.title("Newsletter Unsubscribe")
    root.configure(bg="#2E2E2E")

    global provider_entry
    provider_label = tk.Label(root, text="Newsletter Provider:", bg="#2E2E2E", fg="white")
    provider_label.pack(pady=5)
    provider_entry = tk.Entry(root, bg="#4E4E4E", fg="white")
    provider_entry.pack(pady=5)

    send_button = tk.Button(root, text="Send Unsubscribe Email", command=send_email, bg="#4E4E4E", fg="white")
    send_button.pack(pady=20)

    change_button = tk.Button(root, text="Change Your Data", command=change_data, bg="#4E4E4E", fg="white")
    change_button.pack(pady=5)

    root.mainloop()

# Funktion zum Ändern der gespeicherten Daten
def change_data():
    if os.path.exists('credentials.dat'):
        os.remove('credentials.dat')
    messagebox.showinfo("Info", "Credentials deleted. Please restart the program to enter new credentials.")
    exit()

# Hauptprogramm
if __name__ == "__main__":
    if not os.path.exists('credentials.dat'):
        setup_credentials_gui()
    else:
        try:
            load_credentials()  # Überprüfen, ob die Zugangsdaten gültig sind
            create_gui()  # Haupt-GUI erstellen
        except Exception as e:
            messagebox.showerror("Error", str(e))
            setup_credentials_gui()  # Setup-GUI öffnen, wenn ein Fehler auftritt