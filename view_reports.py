import tkinter as tk
from tkinter import messagebox
from db import get_connection

def open_view_reports_window(user):
    user_id, user_name, _ = user

    report_window = tk.Toplevel()
    report_window.title("Nari Raksha - My Incident History")
    report_window.geometry("820x720")
    report_window.configure(bg="#0f172a")

    tk.Label(
        report_window,
        text=f"REPORT HISTORY: {user_name.upper()}",
        font=("Helvetica", 18, "bold"),
        fg="white",
        bg="#0f172a"
    ).pack(pady=25)

    container = tk.Frame(report_window, bg="#0f172a")
    container.pack(expand=True, fill='both', padx=30, pady=(0, 30))

    report_text = tk.Text(
        container,
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
    report_text.pack(expand=True, fill='both')

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # ---------- OFFLINE REPORTS ----------
        cursor.execute("""
            SELECT o.category, l.name, o.description, o.time
            FROM offline_reports o
            LEFT JOIN locations l ON o.location_id = l.id
            WHERE o.user_id = %s
            ORDER BY o.time DESC
        """, (user_id,))

        report_text.insert(
            tk.END,
            ">>> PHYSICAL INCIDENTS & SAFETY ALERTS <<<\n" + "="*55 + "\n"
        )

        offline = cursor.fetchall()
        if not offline:
            report_text.insert(tk.END, "No physical incidents recorded.\n")
        else:
            for r in offline:
                tag = "[!!! EMERGENCY !!!]" if r[0] == "EMERGENCY" else f"[{r[0]}]"
                report_text.insert(
                    tk.END,
                    f"{tag}\nLocation: {r[1]}\nTime: {r[3]}\nDetails: {r[2]}\n"
                    + "-"*45 + "\n"
                )

        # ---------- ONLINE REPORTS ----------
        cursor.execute("""
            SELECT platform, url, description, time
            FROM online_reports
            WHERE user_id = %s
            ORDER BY time DESC
        """, (user_id,))

        report_text.insert(
            tk.END,
            "\n\n>>> CYBER INCIDENT LOGS <<<\n" + "="*55 + "\n"
        )

        online = cursor.fetchall()
        if not online:
            report_text.insert(tk.END, "No cyber incidents recorded.\n")
        else:
            for r in online:
                report_text.insert(
                    tk.END,
                    f"Platform: {r[0]}\nURL: {r[1]}\nTime: {r[3]}\nDetails: {r[2]}\n"
                    + "-"*45 + "\n"
                )

        conn.close()
        report_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load history: {e}")

    tk.Button(
        report_window,
        text="CLOSE HISTORY",
        command=report_window.destroy,
        bg="#1e293b",
        fg="#38bdf8",
        relief="flat",
        font=("Helvetica", 10, "bold"),
        width=20
    ).pack(pady=15)
