import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from db import get_connection
from safe_route import get_location_graph, dijkstra

def open_safe_route_window(user):
    win = tk.Toplevel()
    win.title("Safe Route Navigation")
    win.geometry("500x650")
    win.configure(bg="#0f172a")

    card = tk.Frame(win, bg="#1e293b", padx=30, pady=30)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(card, text="🗺️ Safe Route Finder",
             font=("Helvetica", 18, "bold"),
             fg="white", bg="#1e293b").pack(pady=15)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, latitude, longitude FROM locations")
    rows = cursor.fetchall()
    conn.close()

    loc_names = [r[1] for r in rows]
    loc_map = {r[1]: r for r in rows}

    tk.Label(card, text="START LOCATION",
             fg="#38bdf8", bg="#1e293b").pack(anchor="w")
    start_var = tk.StringVar(value=loc_names[0])
    ttk.Combobox(card, values=loc_names,
                 textvariable=start_var, width=35).pack(pady=8)

    tk.Label(card, text="DESTINATION",
             fg="#38bdf8", bg="#1e293b").pack(anchor="w")
    end_var = tk.StringVar(value=loc_names[1])
    ttk.Combobox(card, values=loc_names,
                 textvariable=end_var, width=35).pack(pady=8)

    def generate():
        s = loc_map[start_var.get()]
        e = loc_map[end_var.get()]

        graph = get_location_graph()
        path, cost = dijkstra(graph, s[0], e[0])

        if cost == float('inf'):
            messagebox.showerror("No Route", "No safe route found.")
            return

        safety_percent = max(5, min(100, int(100 - (cost / 2000))))

        messagebox.showinfo(
            "Route Analysis",
            f"Safest Route Found\nSafety Score: {safety_percent}%"
        )

        origin = f"{s[2]},{s[3]}"
        dest = f"{e[2]},{e[3]}"
        webbrowser.open(
            f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={dest}"
        )

    tk.Button(card, text="GENERATE SAFEST ROUTE",
              command=generate,
              bg="#38bdf8", fg="#0f172a",
              font=("Helvetica", 12, "bold"),
              width=28, height=2).pack(pady=20)
