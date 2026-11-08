import customtkinter as ctk
from comment_backend import get_all_comments, get_all_reservations, load_json, save_json

comments_file = "comments.json"

def reply_to_comment(comment, parent_window, refresh_callback):
    reply_window = ctk.CTkToplevel(parent_window)
    reply_window.geometry("350x250")
    reply_window.title(f"Reply to {comment['username']}")

    label = ctk.CTkLabel(reply_window, text=f"Reply to user: {comment['username']}", font=("Arial", 13, "bold"))
    label.pack(pady=10)

    text_box = ctk.CTkTextbox(reply_window, width=300, height=100, font=("Arial", 12))
    text_box.pack(pady=10)

    def save_reply():
        reply_text = text_box.get("1.0", "end").strip()
        if not reply_text:
            return
        data = load_json(comments_file)
        for c in data.get("comments", []):
            if c == comment:
                c["reply"] = reply_text
                break
        save_json(comments_file, data)
        reply_window.destroy()
        refresh_callback()  # بعد از ثبت پاسخ، فوراً صفحه کامنت‌ها رفرش می‌شود

    save_button = ctk.CTkButton(reply_window, text="Send Reply", command=save_reply, fg_color="#4477AA", hover_color="#335C88")
    save_button.pack(pady=10)


def open_admin_messages_page(app):
    window = ctk.CTkToplevel(app)
    window.geometry("500x600")
    window.title("Admin - Messages & Reservations")
    window.resizable(False, False)

    tabview = ctk.CTkTabview(window, width=480, height=550)
    tabview.pack(pady=10)

    tab1 = tabview.add("Comments")
    tab2 = tabview.add("Reservations")

    comments_scrollable = ctk.CTkScrollableFrame(tab1, fg_color="white", width=450, height=450)
    comments_scrollable.pack(pady=10)

    def refresh_comments():
        for widget in comments_scrollable.winfo_children():
            widget.destroy()

        comments = get_all_comments()
        for comment in comments:
            comment_frame = ctk.CTkFrame(comments_scrollable, fg_color="#f8f8f8", height=100, width=430)
            comment_frame.pack(pady=5, fill="x", padx=10)
            comment_frame.pack_propagate(False)

            user_label = ctk.CTkLabel(comment_frame, text=f"User: {comment['username']}", font=("Arial", 12, "bold"), text_color="#333333")
            user_label.place(x=15, y=10)

            car_label = ctk.CTkLabel(comment_frame, text=f"Car ID: {comment['car_id']}", font=("Arial", 11), text_color="#666666")
            car_label.place(x=15, y=35)

            comment_text = ctk.CTkLabel(comment_frame, text=f"Comment: {comment['comment']}", font=("Arial", 11), text_color="#666666")
            comment_text.place(x=15, y=55)

            if "reply" in comment:
                reply_label = ctk.CTkLabel(comment_frame, text=f"Admin reply: {comment['reply']}", font=("Arial", 11, "italic"), text_color="#0077AA")
                reply_label.place(x=15, y=75)

            answer_button = ctk.CTkButton(
                comment_frame,
                text="✍",
                font=("Arial", 20, "bold"),
                width=30,
                height=30,
                cursor="hand2",
                fg_color="transparent",
                hover_color="#77A1C4",
                text_color="silver",
                command=lambda c=comment: reply_to_comment(c, window, refresh_comments)
            )
            answer_button.place(x=380, y=10)

    refresh_comments()

    reservations_scrollable = ctk.CTkScrollableFrame(tab2, fg_color="white", width=450, height=450)
    reservations_scrollable.pack(pady=10)

    reservations = get_all_reservations()
    for reservation in reservations:
        reservation_frame = ctk.CTkFrame(reservations_scrollable, fg_color="#f8f8f8", height=70, width=430)
        reservation_frame.pack(pady=5, fill="x", padx=10)
        reservation_frame.pack_propagate(False)

        user_label = ctk.CTkLabel(reservation_frame, text=f"User: {reservation['username']}", font=("Arial", 12, "bold"), text_color="#333333")
        user_label.place(x=15, y=10)

        car_label = ctk.CTkLabel(reservation_frame, text=f"Car: {reservation['car_name']} - {reservation['car_brand']}", font=("Arial", 11), text_color="#666666")
        car_label.place(x=15, y=35)

        car_id_label = ctk.CTkLabel(reservation_frame, text=f"Car ID: {reservation['car_id']}", font=("Arial", 10), text_color="#999999")
        car_id_label.place(x=250, y=35)
