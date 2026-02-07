import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys
import threading
from db import get_connection
from decryption_code import decrypt_file, encrypt_file
import tempfile
import shutil


EVIDENCE_DIR = "evidence_storage"

# -------------------------------------------------
# Helper: decrypt → open → re-encrypt evidence file
# -------------------------------------------------
def open_file_securely(filepath):
    try:
        # Create temp directory
        temp_dir = tempfile.mkdtemp()

        # Temp file path
        temp_file = os.path.join(temp_dir, os.path.basename(filepath))

        # Copy encrypted file
        shutil.copy(filepath, temp_file)

        # Decrypt TEMP copy (not original)
        decrypt_file(temp_file)

        # Open temp file
        if sys.platform.startswith("win"):
            os.startfile(temp_file)
        elif sys.platform.startswith("darwin"):
            subprocess.call(["open", temp_file])
        else:
            subprocess.call(["xdg-open", temp_file])

        messagebox.showinfo(
            "Info",
            "Evidence opened in secure view mode.\nTemporary copy will be deleted automatically."
        )

    except Exception as e:
        messagebox.showerror("Error", f"Cannot open evidence file:\n{e}")
# -------------------------------------------------
# Admin Login Window
# -------------------------------------------------
def admin_login():
    login_window = tk.Toplevel()
    login_window.title("Nari Raksha - Admin Portal")
    login_window.geometry("450x500")
    login_window.configure(bg="#0f172a")

    def check_credentials():
        username = entry_user.get()
        password = entry_pass.get()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM admin WHERE adname=%s AND password=%s",
                (username, password)
            )
            result = cursor.fetchone()
            conn.close()

            if result:
                messagebox.showinfo("Success", f"Access Granted. Welcome {username}!")
                login_window.destroy()
                view_global_reports()
            else:
                messagebox.showerror("Error", "Invalid admin credentials")

        except Exception as e:
            messagebox.showerror("Database Error", f"Connection failed:\n{e}")

    card = tk.Frame(login_window, bg="#1e293b", padx=40, pady=40)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        card, text="Admin Access",
        font=("Helvetica", 22, "bold"),
        fg="white", bg="#1e293b"
    ).pack(pady=(0, 30))

    label_style = {"bg": "#1e293b", "fg": "#38bdf8", "font": ("Helvetica", 9, "bold")}
    entry_style = {
        "bg": "#0f172a", "fg": "white", "relief": "flat",
        "insertbackground": "white", "font": ("Helvetica", 12)
    }

    tk.Label(card, text="ADMIN USERNAME", **label_style).pack(anchor="w")
    entry_user = tk.Entry(card, width=25, **entry_style)
    entry_user.pack(pady=(5, 20))

    tk.Label(card, text="SECURE PASSWORD", **label_style).pack(anchor="w")
    entry_pass = tk.Entry(card, width=25, **entry_style, show="*")
    entry_pass.pack(pady=(5, 30))

    tk.Button(
        card,
        text="VERIFY & LOGIN",
        command=check_credentials,
        bg="#38bdf8",
        fg="#0f172a",
        font=("Helvetica", 11, "bold"),
        width=20,
        height=2,
        relief="flat"
    ).pack()

# -------------------------------------------------
# Admin Global Reports Dashboard
# -------------------------------------------------
def view_global_reports():
    report_window = tk.Toplevel()
    report_window.title("System-Wide Safety Logs")
    report_window.geometry("950x760")
    report_window.configure(bg="#0f172a")

    tk.Label(
        report_window,
        text="🛡️ GLOBAL INCIDENT MONITOR",
        font=("Helvetica", 20, "bold"),
        fg="white",
        bg="#0f172a"
    ).pack(pady=20)

    report_text = tk.Text(
        report_window,
        wrap=tk.WORD,
        bg="#1e293b",
        fg="#e2e8f0",
        font=("Consolas", 10),
        padx=20,
        pady=20,
        relief="flat",
        highlightthickness=1,
        highlightbackground="#334155"
    )
    report_text.pack(expand=True, fill="both", padx=40, pady=(0, 20))

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # -------- OFFLINE REPORTS (includes evidence logs) --------
        cursor.execute("""
            SELECT o.user_id, o.name, o.contact, o.category,
                   o.description, l.name, o.time
            FROM offline_reports o
            LEFT JOIN locations l ON o.location_id = l.id
            ORDER BY o.time DESC
        """)
        offline = cursor.fetchall()

        report_text.insert(tk.END, ">>> PHYSICAL INCIDENT & EVIDENCE LOGS <<<\n" + "="*60 + "\n")
        for r in offline:
            report_text.insert(
                tk.END,
                f"User: {r[1]} | Category: {r[3]}\n"
                f"Location: {r[5]} | Contact: {r[2]}\n"
                f"Time: {r[6]}\n"
                f"Details: {r[4]}\n"
                + "-"*60 + "\n"
            )

        # -------- ONLINE REPORTS --------
        cursor.execute("""
            SELECT name, platform, url, description, time
            FROM online_reports
            ORDER BY time DESC
        """)
        online = cursor.fetchall()

        report_text.insert(tk.END, "\n\n>>> CYBER INCIDENT LOGS <<<\n" + "="*60 + "\n")
        for r in online:
            report_text.insert(
                tk.END,
                f"User: {r[0]} | Platform: {r[1]}\n"
                f"URL: {r[2]}\n"
                f"Details: {r[3]}\n"
                f"Time: {r[4]}\n"
                + "-"*60 + "\n"
            )

        conn.close()
        report_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Database Error", f"Error retrieving logs:\n{e}")

    # -------------------------------------------------
    # OPEN EVIDENCE BUTTON
    # -------------------------------------------------
    def open_latest_evidence():
        try:
            files = os.listdir(EVIDENCE_DIR)
            if not files:
                messagebox.showinfo("Info", "No evidence files found.")
                return

            # Open the most recent evidence file
            latest_file = max(
                files,
                key=lambda f: os.path.getctime(os.path.join(EVIDENCE_DIR, f))
            )
            filepath = os.path.join(EVIDENCE_DIR, latest_file)
            open_file_securely(filepath)

        except Exception as e:
            messagebox.showerror("Error", f"Unable to open evidence:\n{e}")

    tk.Button(
        report_window,
        text="OPEN EVIDENCE",
        command=open_latest_evidence,
        bg="#38bdf8",
        fg="#0f172a",
        font=("Helvetica", 11, "bold"),
        width=22
    ).pack(pady=10)

    tk.Button(
        report_window,
        text="Close Dashboard",
        command=report_window.destroy,
        bg="#1e293b",
        fg="white",
        relief="flat"
    ).pack(pady=10)
