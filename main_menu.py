import tkinter as tk
from tkinter import messagebox

from safety_timer import start_safety_timer
from safe_route_ui import open_safe_route_window
from report_selection import open_report_selection_window
from evidence import open_evidence_vault
from view_reports import open_view_reports_window
from helpline_ui import show_helpline_numbers
from session import current_user


def open_main_menu(user):
    """
    Main dashboard.
    Session remains active until LOGOUT is clicked.
    """
    root = tk.Toplevel()
    root.title("Nari Raksha Dashboard")
    root.geometry("500x850")
    root.configure(bg="#0f172a")

    # ---------- HEADER ----------
    tk.Label(
        root,
        text=f"Welcome, {user[1]}",
        font=("Helvetica", 24, "bold"),
        fg="#38bdf8",
        bg="#0f172a"
    ).pack(pady=30)

    btn_frame = tk.Frame(root, bg="#0f172a")
    btn_frame.pack(expand=True)

    primary = {
        "bg": "#38bdf8",
        "fg": "#0f172a",
        "font": ("Helvetica", 12, "bold"),
        "width": 30,
        "height": 2,
        "relief": "flat"
    }

    secondary = {
        "bg": "#1e293b",
        "fg": "white",
        "font": ("Helvetica", 11),
        "width": 30,
        "height": 2,
        "relief": "flat"
    }

    # ---------- BUTTONS ----------
    tk.Button(
        btn_frame,
        text="⏲️ START SAFETY TIMER",
        command=lambda: start_safety_timer(user),
        **primary
    ).pack(pady=10)

    tk.Button(
        btn_frame,
        text="🚨 EMERGENCY HELPLINE",
        command=show_helpline_numbers,
        bg="#ef4444",
        fg="white",
        font=("Helvetica", 12, "bold"),
        width=30,
        height=2,
        relief="flat"
    ).pack(pady=10)

    tk.Button(
        btn_frame,
        text="🗺️ GET SAFE ROUTE",
        command=lambda: open_safe_route_window(user),
        **secondary
    ).pack(pady=10)

    tk.Button(
        btn_frame,
        text="📢 REPORT INCIDENT",
        command=lambda: open_report_selection_window(user),
        **secondary
    ).pack(pady=10)

    tk.Button(
        btn_frame,
        text="📁 EVIDENCE STORAGE",
        command=lambda: open_evidence_vault(user),
        **secondary
    ).pack(pady=10)

    tk.Button(
        btn_frame,
        text="📜 MY REPORT HISTORY",
        command=lambda: open_view_reports_window(user),
        bg="#0f172a",
        fg="#94a3b8",
        font=("Helvetica", 10, "underline"),
        relief="flat"
    ).pack(pady=20)

    # ---------- LOGOUT (ONLY PLACE WHERE SESSION ENDS) ----------
    def logout():
        current_user[0] = None
        root.destroy()

    tk.Button(
        root,
        text="LOGOUT",
        command=logout,
        bg="#0f172a",
        fg="#ef4444",
        font=("Helvetica", 9),
        relief="flat"
    ).pack(side="bottom", pady=20)

    root.mainloop()
