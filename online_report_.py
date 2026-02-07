import tkinter as tk
from tkinter import messagebox
from db import get_connection

def open_online_report_window(user):
    user_id, name, contact = user

    win = tk.Toplevel()
    win.title("Nari Raksha - Online Harassment Report")
    win.geometry("520x700")
    win.configure(bg="#0f172a")

    card = tk.Frame(win, bg="#1e293b", padx=30, pady=30)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        card,
        text="📱 ONLINE HARASSMENT REPORT",
        font=("Helvetica", 18, "bold"),
        fg="white",
        bg="#1e293b"
    ).pack(pady=15)

    # -------- PLATFORM --------
    tk.Label(card, text="PLATFORM (Instagram / WhatsApp / etc.)",
             fg="#38bdf8", bg="#1e293b").pack(anchor="w")

    platform_entry = tk.Entry(card, width=45,
                              bg="#0f172a", fg="white", relief="flat")
    platform_entry.pack(pady=6)

    # -------- URL --------
    tk.Label(card, text="SCAM / PROFILE URL",
             fg="#38bdf8", bg="#1e293b").pack(anchor="w")

    url_entry = tk.Entry(card, width=45,
                         bg="#0f172a", fg="white", relief="flat")
    url_entry.pack(pady=6)

    # -------- CATEGORY --------
    tk.Label(card, text="CATEGORY",
             fg="#38bdf8", bg="#1e293b").pack(anchor="w")

    category_var = tk.StringVar(value="Cyber Harassment")
    tk.Entry(card, textvariable=category_var,
             width=45, bg="#0f172a", fg="white",
             relief="flat").pack(pady=6)

    # -------- DESCRIPTION --------
    tk.Label(card, text="DESCRIPTION",
             fg="#38bdf8", bg="#1e293b").pack(anchor="w")

    desc_text = tk.Text(card, height=5, width=45,
                        bg="#0f172a", fg="white")
    desc_text.pack(pady=6)

    # -------- SUBMIT --------
    def submit():
        platform = platform_entry.get().strip()
        url = url_entry.get().strip()
        category = category_var.get().strip()
        desc = desc_text.get("1.0", "end").strip()

        if not platform or not url:
            messagebox.showerror("Error", "Platform and URL are required.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO online_reports
            (user_id, name, contact, description, platform, url, category)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            user_id, name, contact,
            desc, platform, url, category
        ))
        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Report Submitted",
            "Online harassment report recorded successfully."
        )
        win.destroy()

    tk.Button(
        card,
        text="SUBMIT REPORT",
        command=submit,
        bg="#38bdf8",
        fg="#0f172a",
        font=("Helvetica", 12, "bold"),
        width=30,
        height=2
    ).pack(pady=20)
