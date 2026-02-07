import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
from db import get_connection
from decryption_code import encrypt_file

EVIDENCE_DIR = "evidence_storage"

def open_evidence_vault(user):
    user_id, name, contact = user

    if not os.path.exists(EVIDENCE_DIR):
        os.makedirs(EVIDENCE_DIR)

    win = tk.Toplevel()
    win.title("Nari Raksha - Evidence Vault")
    win.geometry("500x520")
    win.configure(bg="#0f172a")

    card = tk.Frame(win, bg="#1e293b", padx=30, pady=30)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        card,
        text="📁 EVIDENCE VAULT",
        font=("Helvetica", 18, "bold"),
        fg="white",
        bg="#1e293b"
    ).pack(pady=20)

    def upload():
        file_path = filedialog.askopenfilename(
            title="Select Evidence File",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg"),
                ("Documents", "*.pdf *.doc *.docx"),
                ("Videos", "*.mp4 *.avi"),
                ("All Files", "*.*")
            ]
        )
        if not file_path:
            return

        original_name = os.path.basename(file_path)
        stored_name = f"{user_id}_{original_name}"
        dest_path = os.path.join(EVIDENCE_DIR, stored_name)

        try:
            # Copy + Encrypt
            shutil.copy(file_path, dest_path)
            encrypt_file(dest_path)

            # -------- LOG AS OFFLINE REPORT (FOR USER + ADMIN) --------
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO offline_reports
                (user_id, name, contact, category, description, location_id)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                user_id,
                name,
                contact,
                "EVIDENCE_UPLOADED",
                f"Evidence file uploaded: {stored_name}",
                None
            ))
            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Evidence stored securely and immediately shared with admin."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to store evidence:\n{e}"
            )

    tk.Button(
        card,
        text="UPLOAD EVIDENCE",
        command=upload,
        bg="#38bdf8",
        fg="#0f172a",
        font=("Helvetica", 12, "bold"),
        width=30,
        height=2
    ).pack(pady=20)

    tk.Button(
        card,
        text="CLOSE",
        command=win.destroy,
        bg="#1e293b",
        fg="#38bdf8",
        relief="flat",
        width=20
    ).pack(pady=10)
