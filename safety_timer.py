import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
from db import get_connection

def start_safety_timer(user):
    user_id, user_name, user_contact = user

    win = tk.Toplevel()
    win.title("Nari Raksha – Safety Timer")
    win.geometry("500x700")
    win.configure(bg="#0f172a")

    card = tk.Frame(win, bg="#1e293b", padx=30, pady=30)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        card,
        text="⏱️ SAFETY TIMER",
        font=("Helvetica", 18, "bold"),
        fg="white",
        bg="#1e293b"
    ).pack(pady=15)

    # ---------- FETCH LOCATIONS ----------
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM locations")
    locations = cursor.fetchall()
    conn.close()

    loc_names = [l[1] for l in locations]
    loc_map = {l[1]: l[0] for l in locations}

    # ---------- START LOCATION ----------
    tk.Label(card, text="START LOCATION",
             fg="#38bdf8", bg="#1e293b",
             font=("Helvetica", 9, "bold")).pack(anchor="w")

    start_var = tk.StringVar(value=loc_names[0])
    ttk.Combobox(card, values=loc_names,
                 textvariable=start_var, width=35).pack(pady=6)

    # ---------- DESTINATION ----------
    tk.Label(card, text="DESTINATION",
             fg="#38bdf8", bg="#1e293b",
             font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(10, 0))

    dest_var = tk.StringVar(value=loc_names[1])
    ttk.Combobox(card, values=loc_names,
                 textvariable=dest_var, width=35).pack(pady=6)

    # ---------- TIME ----------
    tk.Label(card, text="TRAVEL TIME (MINUTES)",
             fg="#38bdf8", bg="#1e293b",
             font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(10, 0))

    time_entry = tk.Entry(card, width=40,
                          bg="#0f172a", fg="white", relief="flat")
    time_entry.insert(0, "10")
    time_entry.pack(pady=6)

    # ---------- START WATCHDOG ----------
    def start_watchdog():
        try:
            minutes = int(time_entry.get())
        except:
            messagebox.showerror("Error", "Enter valid time in minutes.")
            return

        start_loc = start_var.get()
        dest_loc = dest_var.get()

        for w in card.winfo_children():
            w.destroy()

        tk.Label(
            card,
            text="🛡️ SAFETY MONITORING ACTIVE",
            font=("Helvetica", 16, "bold"),
            fg="#ef4444",
            bg="#1e293b"
        ).pack(pady=15)

        timer_lbl = tk.Label(
            card,
            text="--:--",
            font=("Helvetica", 48, "bold"),
            fg="#38bdf8",
            bg="#1e293b"
        )
        timer_lbl.pack(pady=20)

        status = {"reached": False}

        def countdown():
            remaining = minutes * 60
            while remaining > 0 and not status["reached"]:
                m, s = divmod(remaining, 60)
                timer_lbl.config(text=f"{m:02d}:{s:02d}")
                time.sleep(1)
                remaining -= 1

            conn = get_connection()
            cursor = conn.cursor()

            if status["reached"]:
                cursor.execute("""
                    INSERT INTO offline_reports
                    (user_id, name, contact, category, description)
                    VALUES (%s,%s,%s,%s,%s)
                """, (
                    user_id, user_name, user_contact,
                    "SAFE",
                    f"User safely reached destination from {start_loc} to {dest_loc}."
                ))
                conn.commit()
                conn.close()
                messagebox.showinfo("Status Logged", "Safe arrival recorded successfully.")
            else:
                cursor.execute("""
                    INSERT INTO offline_reports
                    (user_id, name, contact, category, description)
                    VALUES (%s,%s,%s,%s,%s)
                """, (
                    user_id, user_name, user_contact,
                    "EMERGENCY",
                    f"Safety timer expired. User did not reach destination from {start_loc} to {dest_loc}."
                ))
                conn.commit()
                conn.close()
                messagebox.showerror("Emergency Logged", "Emergency incident has been reported.")

        threading.Thread(target=countdown, daemon=True).start()

        tk.Button(
            card,
            text="✅ I REACHED SAFELY",
            command=lambda: status.update({"reached": True}),
            bg="#4ade80",
            fg="#0f172a",
            font=("Helvetica", 12, "bold"),
            width=28,
            height=2
        ).pack(pady=20)

    tk.Button(
        card,
        text="START SAFETY TIMER",
        command=start_watchdog,
        bg="#38bdf8",
        fg="#0f172a",
        font=("Helvetica", 12, "bold"),
        width=30,
        height=2
    ).pack(pady=25)
