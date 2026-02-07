import tkinter as tk

def show_helpline_numbers():
    win = tk.Toplevel()
    win.title("Emergency Helplines")
    win.geometry("420x600")
    win.configure(bg="#0f172a")

    tk.Label(
        win,
        text="🚨 EMERGENCY HELPLINES",
        font=("Helvetica", 16, "bold"),
        fg="white",
        bg="#ef4444",
        pady=15
    ).pack(fill="x")

    helplines = [
        ("Police Emergency", "100"),
        ("Women Helpline", "1091"),
        ("Women Helpline (India)", "181"),
        ("Child Helpline", "1098"),
        ("Ambulance", "108"),
        ("Cyber Crime", "1930")
    ]

    for name, number in helplines:
        card = tk.Frame(win, bg="#1e293b", padx=20, pady=10)
        card.pack(fill="x", pady=6, padx=20)

        tk.Label(
            card,
            text=name,
            font=("Helvetica", 11, "bold"),
            fg="#38bdf8",
            bg="#1e293b"
        ).pack(anchor="w")

        tk.Label(
            card,
            text=number,
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#1e293b"
        ).pack(anchor="w")
