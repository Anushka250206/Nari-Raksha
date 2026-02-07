import tkinter as tk
from auth import signup, login 
from admin import admin_login 

def main():
    
    root = tk.Tk()
    root.title("Nari Raksha - Women Safety Portal") 
    root.geometry("500x750")
    root.configure(bg="#0f172a") # Professional Deep Navy/Slate

    # --- Header Branding ---
    # Large Shield Icon to establish trust immediately
    tk.Label(root, text="🛡️", font=("Helvetica", 70), bg="#0f172a").pack(pady=(60, 0))
    
    heading = tk.Label(
        root, 
        text="Nari Raksha", 
        font=("Helvetica", 36, "bold"), 
        fg="#38bdf8", # Sky Blue Accent
        bg="#0f172a"
    )
    heading.pack(pady=(0, 5))

    # --- Heading Animation Logic ---
    # Preserved from your original logic to keep the UI engaging
    colors = ["#38bdf8", "#0ea5e9", "#7dd3fc", "#22d3ee", "#06b6d4"]
    color_index = [0]

    def animate_heading():
        heading.config(fg=colors[color_index[0]])
        color_index[0] = (color_index[0] + 1) % len(colors)
        root.after(500, animate_heading)
    
    animate_heading()

    tk.Label(
        root, 
        text="Empowering Safety for Every Woman", 
        font=("Helvetica", 11), 
        fg="#94a3b8", # Muted Slate for subheading
        bg="#0f172a"
    ).pack(pady=(0, 50))

    # --- User Action Section ---
    # Primary button for registration
    tk.Button(
        root, 
        text="CREATE ACCOUNT", 
        command=signup, 
        bg="#38bdf8", 
        fg="#0f172a", 
        font=("Helvetica", 12, "bold"), 
        width=28, 
        height=2, 
        relief="flat",
        activebackground="#7dd3fc"
    ).pack(pady=10)

    # Secondary button for returning users
    tk.Button(
        root, 
        text="USER LOGIN", 
        command=login, 
        bg="#1e293b", # Slate Blue
        fg="white", 
        font=("Helvetica", 11, "bold"), 
        width=28, 
        height=2, 
        relief="flat",
        activebackground="#334155"
    ).pack(pady=10)

    # --- HIGH VISIBILITY ADMIN SECTION ---
    # Distinctive bordered container for authorized access
    admin_frame = tk.Frame(
        root, 
        bg="#1e293b", 
        pady=15, 
        padx=30, 
        highlightbackground="#38bdf8", 
        highlightthickness=1
    )
    admin_frame.pack(side="bottom", pady=50)

    tk.Label(
        admin_frame, 
        text="AUTHORIZED PERSONNEL ONLY", 
        font=("Helvetica", 8, "bold"), 
        fg="#38bdf8", 
        bg="#1e293b"
    ).pack()
    
    # Highly visible admin button
    tk.Button(
        admin_frame, 
        text="🛡️ SYSTEM ADMINISTRATION", 
        command=admin_login, 
        bg="#38bdf8", 
        fg="#0f172a", 
        font=("Helvetica", 10, "bold"),
        relief="flat",
        padx=10
    ).pack(pady=5)

    # Exit Button for clean closure
    tk.Button(
        root, 
        text="EXIT SYSTEM", 
        command=root.quit, 
        bg="#0f172a", 
        fg="#ef4444", # Red for Exit
        font=("Helvetica", 9),
        relief="flat"
    ).place(x=215, y=710)

    root.mainloop()

if __name__ == "__main__":
    main()