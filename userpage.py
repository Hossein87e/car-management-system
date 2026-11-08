import customtkinter as ctk  # import baraye GUI ba customtkinter
from car_backend import get_all_cars  # import tabe baraye gereftan liste mashin ha
from cart_backend import get_cart_items  # import tabe baraye gereftan item ha dar cart
from cart_page import open_cart_page  # import tabe baraye baz kardan safhe cart
from comment_page import (
    open_comment_page,
)  # import tabe baraye baz kardan safhe comment
from PIL import Image  # import PIL baraye load image
import os
from customtkinter import CTkImage  # import CTkImage baraye button icon

app_WIDTH = 450
app_HEIGHT = 600


def setup_app():  # tabe baraye sakhte window asli
    app = ctk.CTk()
    app.resizable(False, False)
    app.title("Car Rental")
    app.configure(fg_color="white")
    x = (app.winfo_screenwidth() // 2) - (app_WIDTH // 2)
    y = (app.winfo_screenheight() // 2) - (app_HEIGHT // 2)
    app.geometry(f"{app_WIDTH}x{app_HEIGHT}+{x}+{y}")
    return app


def logout(app):  # tabe baraye khoroog az user page
    app.destroy()
    import loginsystem

    loginsystem.login_window()  # bargasht be login window


def user_page(app, username):  # tabe asli safhe user
    # Top frame
    top_frame = ctk.CTkFrame(
        app, height=70, width=app_WIDTH, fg_color="#39e65f", corner_radius=3
    )
    top_frame.pack_propagate(False)
    top_frame.pack()

    # Logout icon
    logout_icon = CTkImage(
        light_image=Image.open("logout_photo.png"),
        dark_image=Image.open("logout_photo.png"),
        size=(32, 32),
    )

    # Logout button
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

    # Title
    title_label = ctk.CTkLabel(
        top_frame,
        text="Available Cars",
        font=("Arial Rounded MT Bold", 28, "bold"),
        text_color="white",
    )
    title_label.pack(pady=16, padx=10)

    # Scrollable frame baraye list mashin ha
    cars_scrollable = ctk.CTkScrollableFrame(
        app,
        height=450,
        width=430,
        fg_color="white",
        scrollbar_button_color="#39e65f",
        scrollbar_button_hover_color="#42b85c",
    )
    cars_scrollable.place(y=85, x=10)

    cart_items = get_cart_items()  # gereftan item ha dar cart
    cart_count = len(cart_items)  # tedad item ha

    # Cart button
    cart_button = ctk.CTkButton(
        app,
        text=f"View Cart ({cart_count})",
        fg_color="#008d54",
        hover_color="#035031",
        width=200,
        height=45,
        font=("Arial", 16, "bold"),
        corner_radius=10,
        command=lambda: open_cart_page(app, refresh_cars, username),
    )
    cart_button.place(y=545, x=125)

    # Tabe baraye refresh kardan list mashin ha
    def refresh_cars():
        # pak kardan widget ha
        for widget in cars_scrollable.winfo_children():
            widget.destroy()

        cars = get_all_cars()
        for car in cars:
            car_frame = ctk.CTkFrame(cars_scrollable, fg_color="#f8f8f8", height=120)
            car_frame.pack(pady=8, fill="x")
            car_frame.pack_propagate(False)

            # Name label
            name_label = ctk.CTkLabel(
                car_frame,
                text=f"{car['name']} - {car['brand']}",
                font=("Arial", 16, "bold"),
                text_color="#333333",
            )
            name_label.place(x=15, y=15)

            # Price label
            price_label = ctk.CTkLabel(
                car_frame,
                text=f"$/Day {car['price']}",
                font=("Arial", 14),
                text_color="#008d54",
            )
            price_label.place(x=15, y=45)

            # Available label
            available_label = ctk.CTkLabel(
                car_frame,
                text=f"Available: {car['available']}",
                font=("Arial", 12),
                text_color="#666666",
            )
            available_label.place(x=15, y=70)

            # Year label
            year_label = ctk.CTkLabel(
                car_frame,
                text=f"Year: {car['year']}",
                font=("Arial", 12),
                text_color="#666666",
            )
            year_label.place(x=150, y=70)

            # Add to cart handler
            def add_handler(car_id=car["id"]):
                from cart_backend import add_to_cart

                if add_to_cart(car_id):
                    cart_items = get_cart_items()
                    cart_count = len(cart_items)
                    cart_button.configure(text=f"View Cart ({cart_count})")

            # Add to cart button
            add_button = ctk.CTkButton(
                car_frame,
                text="Add to Cart",
                fg_color="#39e65f",
                width=100,
                height=35,
                command=add_handler,
            )
            add_button.place(x=280, y=40)

            # Comment handler
            def comment_handler(car_id=car["id"], car_name=car["name"]):
                open_comment_page(app, car_id, car_name, username)

            # Comment button
            comment_btn = ctk.CTkButton(
                car_frame,
                text="💬",
                fg_color="transparent",
                text_color="black",
                hover_color="#f2f2f2",
                width=30,
                height=30,
                font=("Arial", 18),
                command=comment_handler,
            )
            comment_btn.place(x=380, y=10)

        # Update cart button
        cart_items = get_cart_items()
        cart_count = len(cart_items)
        cart_button.configure(text=f"View Cart ({cart_count})")

    refresh_cars()  # run baraye load awalie mashin ha


def main_user(username="current_user"):  # tabe asli baraye start user page
    app = setup_app()
    user_page(app, username)
    app.mainloop()


if __name__ == "__main__":
    main_user()
