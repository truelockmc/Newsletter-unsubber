"""
Newsletter Unsubscribe Tool
Dependencies: pip install customtkinter keyring cryptography
"""

import customtkinter as ctk
from tkinter import messagebox
import keyring
import smtplib
import re
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# ── Constants ────────────────────────────────────────────────────────────────
APP_NAME        = "NewsletterUnsub"
KEYRING_EMAIL   = "email"
KEYRING_PASS    = "password"
KEYRING_NAME    = "display_name"
TEMPLATE_FILE   = Path(__file__).parent / "mail_template.txt"

SMTP_MAP = {
    "gmail.com":       ("smtp.gmail.com",        587),
    "yahoo.com":       ("smtp.mail.yahoo.com",   587),
    "outlook.com":     ("smtp.office365.com",    587),
    "hotmail.com":     ("smtp.live.com",         587),
    "aol.com":         ("smtp.aol.com",          587),
    "t-online.de":     ("securesmtp.t-online.de",587),
    "web.de":          ("smtp.web.de",           587),
    "gmx.de":          ("mail.gmx.net",          587),
    "gmx.com":         ("mail.gmx.net",          587),
    "icloud.com":      ("smtp.mail.me.com",      587),
    "freenet.de":      ("mx.freenet.de",         587),
    "posteo.de":       ("posteo.de",             587),
    "protonmail.com":  ("smtp.protonmail.ch",    587),
}

# ── Appearance ────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ── Credential helpers ────────────────────────────────────────────────────────

def save_credentials(email: str, password: str, name: str) -> None:
    """Store credentials securely via the OS keyring."""
    keyring.set_password(APP_NAME, KEYRING_EMAIL, email)
    keyring.set_password(APP_NAME, KEYRING_PASS,  password)
    keyring.set_password(APP_NAME, KEYRING_NAME,  name)


def load_credentials() -> tuple[str, str, str]:
    """Return (email, password, name) from the OS keyring."""
    email    = keyring.get_password(APP_NAME, KEYRING_EMAIL) or ""
    password = keyring.get_password(APP_NAME, KEYRING_PASS)  or ""
    name     = keyring.get_password(APP_NAME, KEYRING_NAME)  or ""
    return email, password, name


def credentials_exist() -> bool:
    email, _, _ = load_credentials()
    return bool(email)


def delete_credentials() -> None:
    for key in (KEYRING_EMAIL, KEYRING_PASS, KEYRING_NAME):
        try:
            keyring.delete_password(APP_NAME, key)
        except keyring.errors.PasswordDeleteError:
            pass


# ── SMTP helper ───────────────────────────────────────────────────────────────

def get_smtp_info(email: str) -> tuple[str, int]:
    domain = email.split("@")[-1].lower()
    if domain in SMTP_MAP:
        return SMTP_MAP[domain]
    raise ValueError(
        f"SMTP-Server fuer '{domain}' nicht bekannt.\n"
        "Bitte tragen Sie die Serverdaten manuell in den Quellcode ein\n"
        "oder wenden Sie sich an Ihren E-Mail-Anbieter."
    )


# ── Mail template ─────────────────────────────────────────────────────────────

def load_template(provider: str, email: str, name: str) -> tuple[str, str]:
    """Return (subject, body) filled from template file."""
    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError(
            f"Vorlagendatei nicht gefunden: {TEMPLATE_FILE}\n"
            "Bitte stellen Sie sicher, dass 'mail_template.txt' im selben\n"
            "Ordner wie dieses Skript liegt."
        )
    raw = TEMPLATE_FILE.read_text(encoding="utf-8")
    lines      = raw.splitlines()
    subject    = lines[0].replace("Subject:", "").strip()
    body_lines = lines[2:]   # skip subject + blank line
    body       = "\n".join(body_lines).format(
        provider=provider,
        email=email,
        name=name,
    )
    return subject, body


# ── Send email ────────────────────────────────────────────────────────────────

def send_email(provider: str) -> None:
    email, password, name = load_credentials()
    smtp_server, smtp_port = get_smtp_info(email)
    subject, body = load_template(provider, email, name)

    msg                   = MIMEMultipart("alternative")
    msg["Subject"]        = subject
    msg["From"]           = f"{name} <{email}>"
    msg["To"]             = provider
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email, password)
        server.sendmail(email, provider, msg.as_string())


# ── Setup window ──────────────────────────────────────────────────────────────

class SetupWindow(ctk.CTk):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.title("Zugangsdaten einrichten")
        self.resizable(False, False)
        self._build_ui()
        self._center()
        self.protocol("WM_DELETE_WINDOW", self._quit)

    def _quit(self):
        self.quit()
        self.destroy()

    def _build_ui(self):
        frame = ctk.CTkFrame(self, corner_radius=16, fg_color="transparent")
        frame.pack(padx=28, pady=24, fill="both", expand=True)

        ctk.CTkLabel(frame, text="⚙  Einrichtung", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(0, 18))

        self.email_var    = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.name_var     = ctk.StringVar()

        _field(frame, "Ihre E-Mail-Adresse",  self.email_var,    placeholder="name@beispiel.de")
        _field(frame, "E-Mail-Passwort",       self.password_var, placeholder="••••••••••", show="•")
        _field(frame, "Ihr Name (für Signatur)",self.name_var,    placeholder="Max Mustermann")

        ctk.CTkLabel(
            frame,
            text="💡 Tipp: Bei Gmail bitte ein App-Passwort verwenden.",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
            wraplength=300,
            justify="left",
        ).pack(anchor="w", padx=2, pady=(4, 14))

        ctk.CTkButton(frame, text="Speichern & weiter", corner_radius=10,
                      command=self._save, height=38).pack(fill="x")

    def _save(self):
        email    = self.email_var.get().strip()
        password = self.password_var.get()
        name     = self.name_var.get().strip()

        if not all([email, password, name]):
            messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen.", parent=self)
            return
        if "@" not in email:
            messagebox.showerror("Fehler", "Bitte eine gültige E-Mail-Adresse eingeben.", parent=self)
            return

        save_credentials(email, password, name)
        self.quit()
        self.destroy()
        self.on_success()

    def _center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - self.winfo_width())  // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")


# ── Main window ───────────────────────────────────────────────────────────────

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Newsletter Abmelden")
        self.resizable(False, False)
        self._build_ui()
        self._center()
        self.protocol("WM_DELETE_WINDOW", self._quit)

    def _quit(self):
        self.quit()
        self.destroy()

    def _build_ui(self):
        frame = ctk.CTkFrame(self, corner_radius=16, fg_color="transparent")
        frame.pack(padx=28, pady=24, fill="both", expand=True)

        ctk.CTkLabel(frame, text="✉  Newsletter abmelden",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(0, 6))

        email, _, name = load_credentials()
        ctk.CTkLabel(
            frame,
            text=f"Gesendet als: {name} <{email}>",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
        ).pack(pady=(0, 18))

        ctk.CTkLabel(frame, text="Absender-Adresse des Newsletters",
                     anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", padx=2)
        self.provider_var = ctk.StringVar()
        ctk.CTkEntry(frame, textvariable=self.provider_var,
                     placeholder_text="newsletter@beispiel.de",
                     corner_radius=10, height=36).pack(fill="x", pady=(4, 16))

        ctk.CTkButton(frame, text="  Abmelde-E-Mail senden", corner_radius=10,
                      height=38, command=self._send).pack(fill="x")

        ctk.CTkButton(frame, text="Zugangsdaten ändern", corner_radius=10,
                      height=32, fg_color="transparent", border_width=1,
                      hover_color=("gray85","gray25"),
                      command=self._change_data).pack(fill="x", pady=(8, 0))

    def _send(self):
        provider = self.provider_var.get().strip()
        if not provider:
            messagebox.showwarning("Hinweis", "Bitte die Newsletter-Adresse eingeben.", parent=self)
            return

        try:
            send_email(provider)
            messagebox.showinfo("Erfolg", f"Abmelde-E-Mail wurde erfolgreich an\n{provider}\ngesendet.", parent=self)
            self.provider_var.set("")
        except Exception as exc:
            messagebox.showerror("Fehler beim Senden", str(exc), parent=self)

    def _change_data(self):
        delete_credentials()
        messagebox.showinfo(
            "Erledigt",
            "Zugangsdaten wurden gelöscht.\nDas Programm wird jetzt neu gestartet.",
            parent=self,
        )
        self.quit()
        self.destroy()
        _run_setup()

    def _center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - self.winfo_width())  // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _field(parent, label: str, var: ctk.StringVar,
           placeholder: str = "", show: str = "") -> None:
    ctk.CTkLabel(parent, text=label, anchor="w",
                 font=ctk.CTkFont(size=13)).pack(fill="x", padx=2)
    kwargs = dict(textvariable=var, placeholder_text=placeholder,
                  corner_radius=10, height=36)
    if show:
        kwargs["show"] = show
    ctk.CTkEntry(parent, **kwargs).pack(fill="x", pady=(4, 12))


def _run_main():
    app = MainWindow()
    app.mainloop()


def _run_setup():
    app = SetupWindow(on_success=_run_main)
    app.mainloop()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if credentials_exist():
        _run_main()
    else:
        _run_setup()
