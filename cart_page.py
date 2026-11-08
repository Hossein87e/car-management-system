import customtkinter as ctk  # import library baraye GUI ba customtkinter
from cart_backend import get_cart_items, remove_from_cart, get_cart_total, clear_cart, reserve_cars  # import tabe ha az cart backend

def open_cart_page(app, refresh_callback, username):  # tabe baraye baz kardan safhe cart
    window = ctk.CTkToplevel(app)  # sakht window jadid (Toplevel)
    window.geometry("400x500")  # size window
    window.title("Shopping Cart")  # title window
    window.resizable(False, False)  # disable resize

    title = ctk.CTkLabel(window, text="Car Reservation", font=("Arial", 20, "bold"))  # label title
    title.pack(pady=20)  # pack ba padding vertical

    cart_items = get_cart_items()  # gereftan hame items dar cart

    if not cart_items:  # agar cart khali bashe
        empty_label = ctk.CTkLabel(window, text="Cart is empty", font=("Arial", 16))  # namayeshe matn khali boodan cart
        empty_label.pack(pady=50)
    else:  # agar cart khali nabashe
        cart_scrollable = ctk.CTkScrollableFrame(  # sakht scrollable frame baraye items
            window, fg_color="white", width=350, height=200
        )
        cart_scrollable.pack(pady=10)

        for item in cart_items:  # halghe baraye namayeshe har item
            item_frame = ctk.CTkFrame(  # frame baraye item
                cart_scrollable, fg_color="#f8f8f8", height=100, width=320
            )
            item_frame.pack(pady=5, fill="x", padx=10)
            item_frame.pack_propagate(False)  # disable automatic resizing

            price_label = ctk.CTkLabel(  # label baraye price
                item_frame,
                text=f"{item['price']}$",
                font=("Arial", 18, "bold"),
                text_color="#333333",
            )
            price_label.place(x=15, y=10)

            dollar_label = ctk.CTkLabel(  # label "dollar"
                item_frame, text="dollar", font=("Arial", 12), text_color="#666666"
            )
            dollar_label.place(x=15, y=30)

            def remove_handler(car_id=item["car_id"]):  # tabe baraye hazf item az cart
                remove_from_cart(car_id)  # hazf item
                window.destroy()  # baste shodan window
                open_cart_page(app, refresh_callback, username)  # refresh safhe cart

            remove_btn = ctk.CTkButton(  # button baraye remove
                item_frame,
                text="Remove",
                fg_color="#ff4444",
                width=60,
                height=25,
                font=("Arial", 10),
                command=remove_handler,  # farakhani remove_handler
            )
            remove_btn.place(x=250, y=15)

            car_name = ctk.CTkLabel(  # namayeshe name va brand khodro
                item_frame,
                text=f"{item['brand']} {item['name']}",
                font=("Arial", 14, "bold"),
                text_color="#333333",
            )
            car_name.place(x=15, y=65)

        total_frame = ctk.CTkFrame(window, fg_color="white", height=60, width=350)  # frame baraye total
        total_frame.pack(pady=10)
        total_frame.pack_propagate(False)

        total_label = ctk.CTkLabel(  # namayeshe total price
            total_frame,
            text=f"Total: {get_cart_total()} dollar",
            font=("Arial", 16, "bold"),
            text_color="#333333",
        )
        total_label.pack(pady=15)

        button_frame = ctk.CTkFrame(window, fg_color="white", height=80, width=350)  # frame baraye button ha
        button_frame.pack(pady=10)
        button_frame.pack_propagate(False)

        def reserve_handler():  # tabe baraye reserve kardan hame items
            success, message = reserve_cars(username)  # farakhani tabe reserve_cars
            if success:  # agar reserve movafagh bood
                window.destroy()  # baste shodan window
                refresh_callback()  # refresh safhe user

        reserve_btn = ctk.CTkButton(  # button baraye reserve
            button_frame,
            text="Complete Reservation",
            fg_color="#39e65f",
            hover_color="#2db84e",
            width=180,
            height=40,
            font=("Arial", 14, "bold"),
            command=reserve_handler,
        )
        reserve_btn.place(x=10, y=20)

        def clear_handler():  # tabe baraye clear kardan cart
            clear_cart()  # pak kardan cart
            window.destroy()  # baste shodan window
            refresh_callback()  # refresh safhe user

        clear_btn = ctk.CTkButton(  # button baraye clear cart
            button_frame,
            text="Clear Cart",
            fg_color="#ff4444",
            hover_color="#cc3333",
            width=140,
            height=40,
            font=("Arial", 12),
            command=clear_handler,
        )
        clear_btn.place(y=20, x=200)
