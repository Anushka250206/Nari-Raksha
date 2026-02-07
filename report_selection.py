# report_selection.py

import tkinter as tk
from online_report_ import open_online_report_window #
from offline_report import open_offline_report_window #

def open_report_selection_window(user):
    """Bridge window for selecting incident type with consistent Modern UI."""
    window = tk.Toplevel()
    window.title("SecureHer - Add Report")
    window.geometry("450x450")
    window.configure(bg="#0f172a") # Standardized Navy Background

    # Center Card Layout
    card = tk.Frame(window, bg="#1e293b", padx=40, pady=40)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        card, 
        text="Report Incident", 
        font=("Helvetica", 20, "bold"), 
        fg="white", 
        bg="#1e293b"
    ).pack(pady=(0, 10))

    tk.Label(
        card, 
        text="Choose the category of the incident", 
        font=("Helvetica", 10), 
        fg="#94a3b8", 
        bg="#1e293b"
    ).pack(pady=(0, 30))

    # High-contrast Button Styles
    button_style = {
        "bg": "#38bdf8", # Sky Blue
        "fg": "#0f172a", # Navy text
        "font": ("Helvetica", 11, "bold"),
        "width": 25,
        "height": 2,
        "relief": "flat",
        "activebackground": "#7dd3fc"
    }

    # Online Report Button
    tk.Button(
        card,
        text="🌐 ONLINE HARASSMENT",
        command=lambda: [window.destroy(), open_online_report_window(user)],
        **button_style
    ).pack(pady=10)

    # Offline Report Button
    tk.Button(
        card,
        text="📍 PHYSICAL INCIDENT",
        command=lambda: [window.destroy(), open_offline_report_window(user)],
        **button_style
    ).pack(pady=10)

    # Return/Cancel Option
    tk.Button(
        card, 
        text="Cancel", 
        command=window.destroy, 
        bg="#1e293b", 
        fg="#64748b", 
        relief="flat",
        font=("Helvetica", 9)
    ).pack(pady=(20, 0))