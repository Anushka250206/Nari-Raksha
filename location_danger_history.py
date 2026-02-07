import tkinter as tk
from db import get_connection

def open_danger_location_ui():
    window = tk.Toplevel()
    window.title("High-Risk Analytics")
    window.geometry("600x650")
    window.configure(bg="#0f172a")

    # Header Card
    header = tk.Frame(window, bg="#1e293b", height=80)
    header.pack(fill="x")
    tk.Label(header, text="🚩 Danger Alert History", font=("Helvetica", 16, "bold"), fg="#ef4444", bg="#1e293b").pack(pady=20)

    # Scrollable area for analytics
    canvas = tk.Canvas(window, bg="#0f172a", highlightthickness=0)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#0f172a")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=20)
    scrollbar.pack(side="right", fill="y")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        # SQL query from your original file preserved
        cursor.execute("""
            SELECT l.name, d.danger_score, d.last_reported
            FROM location_danger d
            JOIN locations l ON d.location_id = l.id
            ORDER BY d.danger_score DESC, d.last_reported DESC
        """)
        
        for row in cursor.fetchall():
            card = tk.Frame(scrollable_frame, bg="#1e293b", padx=15, pady=15)
            card.pack(fill="x", pady=5)
            
            tk.Label(card, text=row[0], font=("Helvetica", 11, "bold"), fg="white", bg="#1e293b").pack(anchor="w")
            
            # Dynamic color logic for danger levels
            score_color = "#ef4444" if row[1] > 5 else "#facc15"
            tk.Label(card, text=f"Danger Score: {row[1]}", font=("Helvetica", 9, "bold"), fg=score_color, bg="#1e293b").pack(anchor="w")
            tk.Label(card, text=f"Last Reported: {row[2]}", font=("Helvetica", 8), fg="#64748b", bg="#1e293b").pack(anchor="e")
            
        conn.close()
    except Exception as e:
        tk.Label(scrollable_frame, text=f"No data available: {e}", fg="gray", bg="#0f172a").pack(pady=20)

    tk.Button(window, text="Close Analytics", command=window.destroy, bg="#0f172a", fg="#94a3b8", relief="flat").pack(pady=10)