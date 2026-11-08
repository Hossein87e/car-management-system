import customtkinter as ctk  # import library baraye GUI ba customtkinter
from comment_backend import add_comment, get_comments_by_car  # import tabe ha az comment backend

def open_comment_page(app, car_id, car_name, username):  # tabe baraye baz kardan safhe comment ha baraye khodro
    window = ctk.CTkToplevel(app)  # sakht window jadid
    window.geometry("400x400")  # size window
    window.title(f"Comments - {car_name}")  # title window ba name khodro
    window.resizable(False, False)  # disable resize

    title = ctk.CTkLabel(window, text=f"Comments for {car_name}", font=("Arial", 18, "bold"))  # label title
    title.pack(pady=15)  # pack ba padding vertical

    comments_scrollable = ctk.CTkScrollableFrame(window, fg_color="white", width=350, height=200)  # scrollable frame baraye comments
    comments_scrollable.pack(pady=10)

    def refresh_comments():  # tabe baraye refresh kardan comments
        for widget in comments_scrollable.winfo_children():  # halghe baraye hazf hame widget ha dakhel scrollable frame
            widget.destroy()  # hazf widget

        comments = get_comments_by_car(car_id)  # gereftan comment ha bar asas car_id
        for comment in comments:  # halghe baraye namayeshe har comment
            comment_frame = ctk.CTkFrame(comments_scrollable, fg_color="#f8f8f8", height=60, width=320)  # frame baraye comment
            comment_frame.pack(pady=5, fill="x", padx=10)
            comment_frame.pack_propagate(False)  # disable automatic resizing

            username_label = ctk.CTkLabel(  # namayeshe username
                comment_frame,
                text=f"User: {comment['username']}",
                font=("Arial", 12, "bold"),
                text_color="#333333"
            )
            username_label.place(x=15, y=10)

            comment_label = ctk.CTkLabel(  # namayeshe matn comment
                comment_frame,
                text=comment["comment"],
                font=("Arial", 11),
                text_color="#666666"
            )
            comment_label.place(x=15, y=35)

    refresh_comments()  # ejra refresh avalieh baraye namayeshe comments

    entry_frame = ctk.CTkFrame(window, fg_color="white", height=100, width=350)  # frame baraye entry comment
    entry_frame.pack(pady=10)
    entry_frame.pack_propagate(False)

    comment_entry = ctk.CTkEntry(  # entry baraye vared kardan comment
        entry_frame,
        placeholder_text="Write your comment...",
        width=300,
        height=40
    )
    comment_entry.pack(pady=10)

    def submit_comment():  # tabe baraye submit kardan comment
        comment_text = comment_entry.get()  # gereftan matn vared shode
        if comment_text.strip():  # agar matn khali nabashe
            add_comment(car_id, "current_user", comment_text)  # ezafe kardan comment
            comment_entry.delete(0, "end")  # pak kardan entry
            refresh_comments()  # refresh namayeshe comments

    submit_button = ctk.CTkButton(
        text="submit button",
        fg_color="#39e65f",
        width=150,
        height=30,
        command=submit_comment
    )
