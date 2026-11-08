import customtkinter as ctk
import os
import json

from add_car_page import open_add_car_page
from edit_car_page import open_edit_car_page
from delete_car_page import open_delete_car_page
from car_backend import get_all_cars
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from admin_messages_page import open_admin_messages_page
from customtkinter import CTkImage
from PIL import Image
app_WIDTH = 450
app_HEIGHT = 600


def load_json(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as file:
        return json.load(file)


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def setup_app():
    app = ctk.CTk()
    app.resizable(False, False)
    app.title("Car Reservation")
    app.configure(fg_color="white")
    x = (app.winfo_screenwidth() // 2) - (app_WIDTH // 2)
    y = (app.winfo_screenheight() // 2) - (app_HEIGHT // 2)
    app.geometry(f"{app_WIDTH}x{app_HEIGHT}+{x}+{y}")
    return app


def logout(app):
    app.destroy()
    import loginsystem

    loginsystem.login_window()


def get_stats():  # tarif tabe braye amar khodro ha
    data = load_json("cars.json")  # khandan file ha va bargardandan an ha
    cars = data.get("cars", [])  # gereftan list mashin ha az kilid "cars"

    # meghdar dehi avalieh
    total_cars = 0
    total_available = 0
    total_reserved = 0

    for car in cars:  # shoroe halghe baraye oubour az tak tak item hy list cars
        total_cars += 1
        total_available += int(car.get("available", "0"))
        total_reserved += int(car.get("reserved", "0"))

    return (
        total_cars,
        total_reserved,
        total_available,
    )  # bazgardni 3 meghdar mohasebeshodeh


def admin_page(app):  # tabee gui admin page
    top_frame = ctk.CTkFrame(
        app, height=70, width=app_WIDTH, fg_color="#39e65f", corner_radius=3
    )
    top_frame.pack_propagate(False)
    top_frame.pack()

    logout_icon = CTkImage(
        light_image=Image.open("project/logout_photo.png"),
        size=(32, 32),
    )

    btn_logout = ctk.CTkButton(
        top_frame,
        text="",
        image=logout_icon,
        width=40,
        height=40,
        fg_color="transparent",
        command=lambda: logout(app),
    )
    btn_logout.place(x=5, y=15)

    title_label = ctk.CTkLabel(
        top_frame,
        text="Admin Panel",
        font=("Arial Rounded MT Bold", 28, "bold"),
        text_color="white",
    )
    title_label.pack(pady=16, padx=10)

    total_cars, total_reserved, total_available = get_stats()

    stats_frame = ctk.CTkFrame(app, fg_color="white", width=440, height=110)
    stats_frame.place(y=85, x=5)
    stats_frame.pack_propagate(False)

    inventory_frame = ctk.CTkFrame(
        stats_frame, fg_color="orange", width=110, height=110
    )
    inventory_frame.pack(side="left", padx=(10, 0))
    inventory_frame.pack_propagate(False)
    inventory_label = ctk.CTkLabel(
        inventory_frame,
        text=total_available,
        font=("Consolas", 33, "bold"),
        text_color="white",
    )
    inventory_label.pack(pady=(15, 0))
    inventory_text = ctk.CTkLabel(
        inventory_frame,
        text="inventory",
        font=("Consolas", 18, "bold"),
        text_color="white",
    )
    inventory_text.pack(pady=1)

    reserved_frame = ctk.CTkFrame(stats_frame, fg_color="orange", width=110, height=110)
    reserved_frame.place(anchor="center", x=220, y=55)
    reserved_frame.pack_propagate(False)
    reserved_label = ctk.CTkLabel(
        reserved_frame,
        text=total_reserved,
        font=("Consolas", 33, "bold"),
        text_color="white",
    )
    reserved_label.pack(pady=(15, 0))
    reserved_text = ctk.CTkLabel(
        reserved_frame,
        text="reserved\nCars",
        font=("Consolas", 18, "bold"),
        text_color="white",
    )
    reserved_text.pack(pady=1)

    all_cars_frame = ctk.CTkFrame(stats_frame, fg_color="orange", width=110, height=110)
    all_cars_frame.pack(side="right", padx=(0, 10))
    all_cars_frame.pack_propagate(False)
    all_cars_label = ctk.CTkLabel(
        all_cars_frame,
        text=total_cars,
        font=("Consolas", 33, "bold"),
        text_color="white",
    )
    all_cars_label.pack(pady=(15, 0))
    all_cars_text = ctk.CTkLabel(
        all_cars_frame,
        text="All\nCars",
        font=("Consolas", 18, "bold"),
        text_color="white",
    )
    all_cars_text.pack(pady=1)

    chart_frame = ctk.CTkFrame(app, fg_color="silver", width=460, height=190)
    chart_frame.place(y=200, x=5)
    chart_frame.pack_propagate(False)
    plt.figure(figsize=(4, 2))
    plt.grid(visible=True, color="gray", linestyle="--", linewidth=0.5)

    def update_chart():  # update matplotlib

        # gereftan amar tazeh ba seda kardan tabee get stats
        total_cars, total_reserved, total_available = get_stats()

        plt.clf()  # pak kardan shekl (clear figure) dar matplotlib ta nemoodar ghabli hazf shavad

        categories = [
            "All Cars",
            "Reserved",
            "Available",
        ]  # tarif daste bandy hay mehvar x
        values = [
            total_cars,
            total_reserved,
            total_available,
        ]  # tarif meghdar hay motanazer ba har daste baray rasm soton

        plt.bar(
            categories, values, color="lightgreen", width=0.3
        )  # rasm nemoodar sootoni

        plt.ylabel("Count")  # title mehvar y ha

        canvas = FigureCanvasTkAgg(
            plt.gcf(), chart_frame
        )  # sakht yeck canvas az shecl jari (get current figure) ke ghabel joda sazi az ctk ast va master an chart fraeast
        canvas.get_tk_widget().pack(
            fill="both", expand=True
        )  # gereftan vidget tk marboot be canvas va ghrar dadan an dakhel chart frame
        canvas.draw()  # tarsim nahaiy chart

    update_chart()  # ejray avalieh tabee ta nemoodar dar zaman namyesh app baz shvad

    car_box = ctk.CTkScrollableFrame(
        app,
        height=200,
        width=260,
        fg_color="white",
        scrollbar_button_color="#39e65f",
        scrollbar_button_hover_color="#42b85c",
    )
    car_box.place(y=390, x=155)

    def refresh_carbox():  # tabeey ke carbox ro be rooz resani maikonad
        for (
            widget
        ) in (
            car_box.winfo_children()
        ):  # baray widget hay dakhel car box (ctklabel or frame):
            widget.destroy()  # tamam widget hay dakhel anro hazf migirad va sepas hazf mikonad

        cars = get_all_cars()  # list khodro haro az backend migreh
        for car in cars:  # shoroe halghe roy har khodro dar list
            frm_cars = ctk.CTkFrame(car_box, fg_color="#f8f8f8", height=50)
            frm_cars.pack(pady=6, fill="x")  # fill = keshesh ofoghi
            frm_cars.pack_propagate(False)

            car_box_text = ctk.CTkLabel(
                frm_cars,
                text=f"{car['name']} - Available: {car['available']} - Reserved: {car['reserved']}",
                font=("Arial", 14),
                text_color="#008d54",
            )
            car_box_text.pack(anchor="w", padx=10, pady=10)

    def refresh_page():  # tabee ke kol safheh ro be rozresany mikonad
        total_cars, total_reserved, total_available = get_stats()  # gereftan amar jadid

        # tanzim matn label ha
        all_cars_label.configure(text=total_cars)
        reserved_label.configure(text=total_reserved)
        inventory_label.configure(text=total_available)

        refresh_carbox()

    refresh_carbox()

    btn_add = ctk.CTkButton(
        app,
        text="add a car",
        hover_color="#035031",
        fg_color="#008d54",
        corner_radius=10,
        command=lambda: open_add_car_page(app, refresh_page),
    )
    btn_add.place(y=425, x=5)

    btn_edit = ctk.CTkButton(
        app,
        text="edit car",
        hover_color="#035031",
        fg_color="#008d54",
        corner_radius=10,
        command=lambda: open_edit_car_page(app, refresh_page),
    )
    btn_edit.place(y=458, x=5)

    btn_delete = ctk.CTkButton(
        app,
        text="remove cars",
        hover_color="#035031",
        fg_color="#008d54",
        corner_radius=10,
        command=lambda: open_delete_car_page(app, refresh_page),
    )
    btn_delete.place(y=493, x=5)

    comment_icon = CTkImage(
        light_image=Image.open("project/comment_icon.png"),
        size=(32, 32),
    )

    btn_messages = ctk.CTkButton(
        app,
        text="",
        image=comment_icon,
        width=40,
        height=40,
        fg_color="#39e65f",
        bg_color="#39e65f",
        hover_color="#39e65f",
        command=lambda: open_admin_messages_page(app),
    )
    btn_messages.place(x=400, y=15)


def main_admin():  # tabeey ke barnameh ro baz mikonad
    app = setup_app()  # gui asli ro msaze
    admin_page(app)  # sakht va namayesh safhe admin dar pangereh sakhte shode
    app.mainloop()


if (
    __name__ == "__main__"
):  # sharti ke barresi mikonad aia in file mostaghiman ejra shode ya be soorat majoul import shode
    main_admin()
