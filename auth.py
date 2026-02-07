import tkinter as tk
from tkinter import messagebox
from db import get_connection
from session import current_user # Global session tracking
import main_menu
import re

def signup():
    """Sign up window with modern card UI and validation."""
    def submit_signup():
        name = name_entry.get().strip()
        contact = contact_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        # Input Validation
        if not re.match(r"^[0-9]{10}$", contact):
            messagebox.showerror("Error", "Enter a valid 10-digit contact number.")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Enter a valid email address.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Check for existing users
            cursor.execute("SELECT * FROM users WHERE contact=%s", (contact,))
            if cursor.fetchone():
                messagebox.showerror("Error", "User already exists.")
                return

            # Registration Logic
            cursor.execute("INSERT INTO users (name, contact, email, password) VALUES (%s, %s, %s, %s)", 
                           (name, contact, email, password))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Registration complete. Please login.")
            signup_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    signup_window = tk.Toplevel()
    signup_window.title("SecureHer - Join Us")
    signup_window.geometry("450x600")
    signup_window.configure(bg="#0f172a") # Deep Slate Navy

    # Center Card
    card = tk.Frame(signup_window, bg="#1e293b", padx=30, pady=30)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(card, text="Create Account", font=("Helvetica", 18, "bold"), fg="white", bg="#1e293b").pack(pady=(0, 20))

    # Styling labels and entries for a premium look
    label_style = {"bg": "#1e293b", "fg": "#38bdf8", "font": ("Helvetica", 9, "bold")}
    entry_style = {"bg": "#0f172a", "fg": "white", "relief": "flat", "insertbackground": "white", "width": 30}

    # Name
    tk.Label(card, text="FULL NAME", **label_style).pack(anchor="w")
    name_entry = tk.Entry(card, **entry_style)
    name_entry.pack(pady=(5, 15))

    # Contact
    tk.Label(card, text="CONTACT NUMBER", **label_style).pack(anchor="w")
    contact_entry = tk.Entry(card, **entry_style)
    contact_entry.pack(pady=(5, 15))

    # Email
    tk.Label(card, text="EMAIL ADDRESS", **label_style).pack(anchor="w")
    email_entry = tk.Entry(card, **entry_style)
    email_entry.pack(pady=(5, 15))

    # Password
    tk.Label(card, text="PASSWORD", **label_style).pack(anchor="w")
    password_entry = tk.Entry(card, **entry_style, show="*")
    password_entry.pack(pady=(5, 20))

    tk.Button(card, text="REGISTER NOW", command=submit_signup, bg="#38bdf8", fg="#0f172a", 
              font=("Helvetica", 11, "bold"), width=20, height=2, relief="flat").pack()

def login():
    """Login window that anchors the user session globally."""
    def submit_login():
        name = name_entry.get().strip()
        password = password_entry.get().strip()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Verify credentials
            cursor.execute("SELECT user_id, name, contact FROM users WHERE name=%s AND password=%s", (name, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                # Update global session to prevent logout bugs
                current_user[0] = user
                messagebox.showinfo("Welcome", f"Access granted, {user[1]}!")
                login_window.destroy()
                main_menu.open_main_menu(user)
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {e}")

    login_window = tk.Toplevel()
    login_window.title("SecureHer - Access")
    login_window.geometry("450x500")
    login_window.configure(bg="#0f172a")

    card = tk.Frame(login_window, bg="#1e293b", padx=30, pady=30)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(card, text="User Login", font=("Helvetica", 18, "bold"), fg="white", bg="#1e293b").pack(pady=(0, 25))

    label_style = {"bg": "#1e293b", "fg": "#38bdf8", "font": ("Helvetica", 9, "bold")}
    entry_style = {"bg": "#0f172a", "fg": "white", "relief": "flat", "insertbackground": "white", "width": 30}

    tk.Label(card, text="USER NAME", **label_style).pack(anchor="w")
    name_entry = tk.Entry(card, **entry_style)
    name_entry.pack(pady=(5, 15))

    tk.Label(card, text="PASSWORD", **label_style).pack(anchor="w")
    password_entry = tk.Entry(card, **entry_style, show="*")
    password_entry.pack(pady=(5, 25))

    tk.Button(card, text="ENTER DASHBOARD", command=submit_login, bg="#38bdf8", fg="#0f172a", 
              font=("Helvetica", 11, "bold"), width=20, height=2, relief="flat").pack()