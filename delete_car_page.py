import customtkinter as ctk  # import library baraye GUI ba customtkinter
from tkinter import messagebox  # import library baraye messagebox
from car_backend import get_all_cars, delete_car  # import tabe ha az backend baraye gereftan va hazf khodro

def open_delete_car_page(app, refresh_callback):  # tabe baraye baz kardan safhe delete car
    window = ctk.CTkToplevel(app)  # sakht window jadid
    window.geometry("400x400")  # size window
    window.title("Delete Car")  # title window
    window.resizable(False, False)  # disable resize

    title = ctk.CTkLabel(window, text="Delete Car", font=("Arial", 20, "bold"), text_color="red")  # label title
    title.pack(pady=20)

    cars = get_all_cars()  # gereftan hame khodro ha

    if not cars:  # agar khodro vojood nadashte bashe
        messagebox.showinfo("Info", "No cars to delete")  # namayeshe payam
        window.destroy()  # close window
        return  # payan tabe

    scroll_frame = ctk.CTkScrollableFrame(window, width=350, height=250)  # scrollable frame baraye list khodro ha
    scroll_frame.pack(pady=20)

    def delete_selected_car(car_id):  # tabe baraye hazf khodro entekhab shode
        result = messagebox.askyesno("Confirm", "Are you sure you want to delete this car?")  # confirm hazf
        if result:  # agar yes entekhab shode
            if delete_car(car_id):  # hazf khodro az backend
                messagebox.showinfo("Success", "Car deleted")  # payam movafaghiat
                refresh_callback()  # refresh safheh admin
                window.destroy()  # close window

    for car in cars:  # halghe baraye namayeshe hame khodro ha
        car_frame = ctk.CTkFrame(scroll_frame, fg_color="white")  # frame baraye har khodro
        car_frame.pack(fill="x", pady=5, padx=5)

        info_frame = ctk.CTkFrame(car_frame, fg_color="transparent")  # frame baraye text khodro
        info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        car_name = ctk.CTkLabel(info_frame, text=f"{car['name']} ({car['brand']})",
                               font=("Arial", 14, "bold"), text_color="black")  # label baraye name va brand
        car_name.pack(anchor="w")

        car_details = ctk.CTkLabel(info_frame, text=f"Year: {car['year']} | Available: {car['available']}",
                                   font=("Arial", 11), text_color="gray")  # label baraye sal va available
        car_details.pack(anchor="w")

        btn_delete = ctk.CTkButton(car_frame, text="Delete", width=80, height=30,
                                   fg_color="red", hover_color="#8B0000",
                                   command=lambda cid=car["id"]: delete_selected_car(cid))  # button hazf
        btn_delete.pack(side="right", padx=10, pady=10)

    btn_close = ctk.CTkButton(window, text="Close", command=window.destroy,
                             width=150, fg_color="gray")  # button close window
    btn_close.pack(pady=10)
