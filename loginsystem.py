import customtkinter as ctk  # import baraye GUI ba customtkinter
import os  # baraye check file ha va path
import json  # baraye load va save JSON
from tkinter import messagebox  # baraye namayeshe payam ha
import adminpage  # import safhe admin
from PIL import Image, ImageTk  # import baraye load image
import userpage  # import safhe user

def login_window():  # tabe baraye window login
    app_width, app_height = 450, 600  # size window
    app = ctk.CTk()  # sakht app
    app.resizable(False, False)  # disable resize
    app.title("Car Reservation")  # title
    app.configure(fg_color="white")  # background color

    # center kardan window
    x = (app.winfo_screenwidth() // 2) - (app_width // 2)
    y = (app.winfo_screenheight() // 2) - (app_height // 2)
    app.geometry(f"{app_width}x{app_height}+{x}+{y}")

    # Top frame
    frm_top = ctk.CTkFrame(
        app, height=70, width=app_width, fg_color="#39e65f", corner_radius=3
    )
    frm_top.pack_propagate(False)
    frm_top.pack()

    # Top label
    lbl_top = ctk.CTkLabel(
        frm_top,
        text="Login Page",
        font=("Arial Rounded MT Bold", 28, "bold"),
        text_color="white",
    )
    lbl_top.pack(pady=16, padx=10)

    # Top image
    bg_path = "project/car_photo.png"
    if os.path.exists(bg_path):
        bg_image = Image.open(bg_path).resize((130, 130))  # resize image
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = ctk.CTkLabel(app, image=bg_photo, text="", width=30, height=40)
        bg_label.image = bg_photo
        bg_label.place(x=(app_width // 2) - 60, y=130)
        bg_label.lower()
    else:
        print(f"Background image not found at {bg_path}")

    # Username label and entry
    lbl_username = ctk.CTkLabel(app, text="USERNAME :", font=("Helvetica", 14))
    lbl_username.pack(pady=(210, 0), padx=90, anchor="w")

    ent_username = ctk.CTkEntry(
        app, placeholder_text="Enter your username", width=250, border_width=1
    )
    ent_username.pack(pady=(1, 0), padx=90, anchor="w")

    # Password label and entry
    lbl_password = ctk.CTkLabel(app, text="PASSWORD :", font=("Helvetica", 14))
    lbl_password.pack(pady=(20, 0), padx=90, anchor="w")

    ent_password = ctk.CTkEntry(
        app, placeholder_text="Enter your password", width=250, border_width=1, show="*"
    )
    ent_password.pack(pady=1, padx=90, anchor="w")

    # Buttons
    btn_login = ctk.CTkButton(
        app,
        text="Log In",
        font=("Helvetica", 16),
        hover_color="#39e65f",
        fg_color="#2eb74a",
        width=80,
        height=30,
        corner_radius=8,
        cursor="hand2",
    )
    btn_login.place(x=120, y=440)

    btn_signup = ctk.CTkButton(
        app,
        text="Sign Up",
        font=("Helvetica", 16),
        fg_color="#39b4e6",
        hover_color="#2e8cb7",
        width=80,
        height=30,
        corner_radius=8,
        cursor="hand2",
    )
    btn_signup.place(x=230, y=440)

    btn_adminlog = ctk.CTkButton(
        app,
        text="Admin Login",
        font=("Helvetica", 16),
        fg_color="#39b4e6",
        hover_color="#2e8cb7",
        width=120,
        height=30,
        corner_radius=8,
        cursor="hand2",
    )
    btn_adminlog.pack(anchor="center", pady=70)

    # File paths
    user_file = "user.json"
    admin_file = "admin.json"

    # JSON helpers
    def json_file(filename):  # tabe baraye load JSON
        if not os.path.exists(filename):
            return {}
        with open(filename, "r") as myfile:
            try:
                return json.load(myfile)
            except FileNotFoundError:
                return {}

    def save(filename, data):  # tabe baraye save JSON
        with open(filename, "w") as myfile:
            json.dump(data, myfile)

    # User login
    def login():
        username = ent_username.get()
        password = ent_password.get()
        users = json_file(user_file)
        if username in users and users[username] == password:
            messagebox.showinfo("Login Successful", "Welcome!")
            app.destroy()
            userpage.main_user(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    # User signup
    def signup():
        username = ent_username.get()
        password = ent_password.get()
        if not username or not password:
            messagebox.showerror("Sign Up Failed", "Username and password required.")
            return
        users = json_file(user_file)
        if username in users:
            messagebox.showerror("Sign Up Failed", "Username already exists.")
            return
        users[username] = password
        save(user_file, users)
        messagebox.showinfo("Sign Up", "Account created successfully.")
        app.destroy()
        userpage.main_user()

    # Admin login
    def admin_login():
        username = ent_username.get()
        password = ent_password.get()
        admins = json_file(admin_file)
        if username in admins and admins[username] == password:
            messagebox.showinfo("Admin Login", "Welcome, admin!")
            app.destroy()
            adminpage.main_admin()
        else:
            messagebox.showerror("Admin Login Failed", "Invalid admin credentials.")

    # Connect buttons to functions
    btn_login.configure(command=login)
    btn_signup.configure(command=signup)
    btn_adminlog.configure(command=admin_login)

    app.mainloop()  # start main loop

if __name__ == "__main__":
    login_window()  # run login window
