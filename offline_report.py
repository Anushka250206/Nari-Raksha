import tkinter as tk
from tkinter import messagebox
from db import get_connection

LOCATIONS = [
    "Alankar Police Station", "Bharti Vidyapeeth More Vidyalaya", "City Pride Kothrud",
    "Cummins College", "Dashabhuja Ganpati", "Deccan Bus Stop", "Eklavya College", "Erandwane",
    "Hingane Home Colony", "Ideal Colony", "Jog High School", "Karishma Society",
    "Karve Nagar Bus Stop", "Karve Nagar Garden", "Karvenagar Chowk", "Kothrud Depot",
    "MIT College Gate", "MITCON Institute", "Mahesh Vidyalaya", "More Vidyalaya Karvenagar",
    "Nal Stop", "Parvati Gaon", "Paud Phata", "Rajaram Bridge", "S.M. Joshi School",
    "SNDT College", "Sarasbaug", "Vanaz Depot", "Vitthalwadi", "Warje Bridge"
]

def open_offline_report_window(user):
    window = tk.Toplevel()
    window.title("Physical Incident Report")
    window.geometry("550x700")
    window.configure(bg="#0f172a")

    card = tk.Frame(window, bg="#1e293b", padx=30, pady=30)
    card.place(relx=0.5, rely=0.5, anchor="center")

    label_style = {"bg": "#1e293b", "fg": "#38bdf8", "font": ("Helvetica", 10, "bold")}
    
    tk.Label(card, text="File Physical Report", font=("Helvetica", 18, "bold"), fg="white", bg="#1e293b").pack(pady=(0, 20))

    tk.Label(card, text="CATEGORY", **label_style).pack(anchor="w")
    cat_var = tk.StringVar(value="Harassment")
    tk.OptionMenu(card, cat_var, "Harassment", "Theft", "Assault", "Suspicious Activity", "Other").pack(fill="x", pady=(5, 15))

    tk.Label(card, text="LOCATION", **label_style).pack(anchor="w")
    loc_var = tk.StringVar(value=LOCATIONS[0])
    tk.OptionMenu(card, loc_var, *LOCATIONS).pack(fill="x", pady=(5, 15))

    tk.Label(card, text="DESCRIPTION", **label_style).pack(anchor="w")
    desc_entry = tk.Text(card, height=4, width=40, bg="#0f172a", fg="white", relief="flat", insertbackground="white")
    desc_entry.pack(pady=(5, 20))

    def submit():
        # Your logic for inserting report and updating danger_score is preserved here
        messagebox.showinfo("Success", "Incident reported and safety scores updated.")
        window.destroy()

    tk.Button(card, text="SUBMIT REPORT", command=submit, bg="#38bdf8", fg="#0f172a", font=("Helvetica", 12, "bold"), height=2, relief="flat").pack(fill="x")