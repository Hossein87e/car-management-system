# add_car_page.py
import customtkinter as ctk  # import library baraye GUI ba customtkinter
from tkinter import messagebox  # import library baraye messagebox (popup ha)
from car_backend import add_car  # import function add_car az backend


def open_add_car_page(app, refresh_callback):  # tabe baraye baz kardan safhe Add Car
    window = ctk.CTkToplevel(
        app
    )  # sakht yek Toplevel window (window jadid baraye add car)
    window.geometry("350x400")  # size window
    window.title("Add Car")  # title window
    window.resizable(False, False)  # gharaar dadan window ghable resize nabashad

    title = ctk.CTkLabel(
        window, text="Add New Car", font=("Arial", 20, "bold")
    )  # label title
    title.pack(pady=20)  # pack kardan label ba padding vertical

    entry_name = ctk.CTkEntry(
        window, placeholder_text="Car Name", width=250, height=35
    )  # entry baraye name khodro
    entry_name.pack(pady=5)

    entry_brand = ctk.CTkEntry(
        window, placeholder_text="Brand", width=250, height=35
    )  # entry baraye brand khodro
    entry_brand.pack(pady=5)

    entry_year = ctk.CTkEntry(
        window, placeholder_text="Year", width=250, height=35
    )  # entry baraye year khodro
    entry_year.pack(pady=5)

    entry_price = ctk.CTkEntry(
        window, placeholder_text="price in $", width=250, height=35
    )  # entry baraye price
    entry_price.pack(pady=5)

    entry_available = ctk.CTkEntry(
        window, placeholder_text="Available", width=250, height=35
    )  # entry baraye available
    entry_available.pack(pady=5)

    def save_car():  # tabe baraye zakhire kardan khodro
        name = entry_name.get()  # gereftan matn az entry
        brand = entry_brand.get()
        year = entry_year.get()
        price = entry_price.get()
        available = entry_available.get()

        if (
            not name or not brand or not year or not price or not available
        ):  # agar hich field khali bashe
            messagebox.showerror("Error", "Please fill all fields")  # namayeshe error
            return  # exit tabe

        try:  # try baraye tabdil string be int
            year = int(year)
            price = int(price)
            available = int(available)
        except:
            messagebox.showerror(
                "Error", "Year and Available must be numbers"
            )  # namayeshe error agar tabdil nashod
            return

        add_car(
            name, brand, year, price, available
        )  # farakhani tabe add_car az backend
        messagebox.showinfo(
            "Success", "Car added successfully"
        )  # namayeshe message baraye movafaghiat
        refresh_callback()  # farakhani callback baraye update kardan safhe admin
        window.destroy()  # bastan window Add Car

    button_frame = ctk.CTkFrame(
        window, fg_color="transparent"
    )  # sakht frame baraye button ha
    button_frame.pack(pady=20)

    btn_save = ctk.CTkButton(  # button baraye save kardan khodro
        button_frame,
        text="Save Car",
        command=save_car,  # farakhani tabe save_car
        width=100,
        height=35,
        fg_color="#008d54",
    )
    btn_save.pack(side="left", padx=5)  # pack button dar frame, chap

    btn_cancel = ctk.CTkButton(  # button baraye cancel kardan
        button_frame,
        text="Cancel",
        command=window.destroy,  # baste shodan window
        width=100,
        height=35,
        fg_color="gray",
    )
    btn_cancel.pack(side="right", padx=5)  # pack button dar frame, rast
