import customtkinter as ctk  # import library baraye GUI ba customtkinter
from tkinter import messagebox  # import baraye namayeshe payam ha
from car_backend import get_all_cars, get_car_by_id, edit_car  # import tabe ha az backend

def open_edit_car_page(app, refresh_callback):  # tabe baraye baz kardan safhe edit car
    window = ctk.CTkToplevel(app)  # sakht window jadid
    window.geometry("400x500")  # size window
    window.title("Edit Car")  # title window
    window.resizable(False, False)  # disable resize

    title = ctk.CTkLabel(window, text="Edit Car", font=("Arial", 20, "bold"))  # label title
    title.pack(pady=20)

    cars = get_all_cars()  # gereftan hame khodro ha

    if not cars:  # agar khodro vojood nadashte bashe
        messagebox.showinfo("Info", "No cars to edit")  # namayeshe payam
        window.destroy()  # close window
        return  # payan tabe

    select_label = ctk.CTkLabel(window, text="Select Car:", font=("Arial", 14))  # label baraye select
    select_label.pack(pady=5)

    car_names = [f"{car['name']} - {car['brand']}" for car in cars]  # list name va brand khodro ha
    selected_car = ctk.StringVar(value=car_names[0])  # variable baraye combobox

    car_menu = ctk.CTkComboBox(
        window,
        values=car_names,
        variable=selected_car,
        width=300,
        height=35,
        state="readonly",  # readonly baraye prevent editing
    )
    car_menu.pack(pady=5)

    # entry ha baraye edit kardan field ha
    entry_name = ctk.CTkEntry(window, placeholder_text="Car Name", width=300, height=35)
    entry_name.pack(pady=5)

    entry_brand = ctk.CTkEntry(window, placeholder_text="Brand", width=300, height=35)
    entry_brand.pack(pady=5)

    entry_year = ctk.CTkEntry(window, placeholder_text="Year", width=300, height=35)
    entry_year.pack(pady=5)

    entry_price = ctk.CTkEntry(window, placeholder_text="price in $ ", width=300, height=35)
    entry_price.pack(pady=5)

    entry_available = ctk.CTkEntry(window, placeholder_text="Available", width=300, height=35)
    entry_available.pack(pady=5)

    def load_car_data():  # tabe baraye load kardan data khodro entekhab shode
        car_text = selected_car.get()  # gereftan text entekhab shode
        selected_index = car_names.index(car_text)  # index khodro entekhab shode
        car = cars[selected_index]  # gereftan dict khodro

        entry_name.delete(0, "end")  # clear entry
        entry_name.insert(0, car["name"])  # insert name
        entry_brand.delete(0, "end")
        entry_brand.insert(0, car["brand"])
        entry_year.delete(0, "end")
        entry_year.insert(0, str(car["year"]))
        entry_price.delete(0, "end")
        entry_price.insert(0, str(car["price"]))
        entry_available.delete(0, "end")
        entry_available.insert(0, str(car["available"]))

    btn_load = ctk.CTkButton(
        window, text="Load Car Data", command=load_car_data, width=300, fg_color="blue"  # button baraye load data
    )
    btn_load.pack(pady=10)

    def save_changes():  # tabe baraye save kardan taghirat
        car_text = selected_car.get()
        selected_index = car_names.index(car_text)
        car_id = cars[selected_index]["id"]  # gereftan id khodro

        name = entry_name.get()  # gereftan values jadid az entry ha
        brand = entry_brand.get()
        year = entry_year.get()
        price = entry_price.get()
        available = entry_available.get()

        if not name or not brand or not year or not price or not available:  # check fields
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:  # tabdil be int
            year = int(year)
            price = int(price)
            available = int(available)
        except:
            messagebox.showerror("Error", "Year and Available must be numbers")
            return

        if edit_car(car_id, name, brand, year, price, available):  # save be backend
            messagebox.showinfo("Success", "Car edited successfully")
            refresh_callback()  # refresh safhe admin
            window.destroy()  # close window

    button_frame = ctk.CTkFrame(window, fg_color="transparent")  # frame baraye button ha
    button_frame.pack(pady=20)

    btn_save = ctk.CTkButton(
        button_frame,
        text="Save Changes",
        command=save_changes,
        width=120,
        fg_color="#008d54",  # button save
    )
    btn_save.pack(side="left", padx=5)

    btn_cancel = ctk.CTkButton(
        button_frame, text="Cancel", command=window.destroy, width=120, fg_color="gray"  # button cancel
    )
    btn_cancel.pack(side="right", padx=5)
