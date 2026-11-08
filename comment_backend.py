import json  # import library baraye khandan va neveshtan file JSON
import os    # import library baraye barresi vojood file ha

comments_file = "comments.json"  # file JSON baraye zakhire comment ha
reservations_file = "reservations.json"  # file JSON baraye zakhire reservation ha

def load_json(filename):  # tabe baraye load kardan data az file JSON
    if not os.path.exists(filename):  # agar file vojood nadashte bashe
        return {}  # dictionary khali barmigardanim
    with open(filename, "r") as file:  # baz kardan file dar mode read
        return json.load(file)  # load kardan data va barmigardan dictionary

def save_json(filename, data):  # tabe baraye zakhire kardan data dar file JSON
    with open(filename, "w") as file:  # baz kardan file dar mode write
        json.dump(data, file, indent=4)  # neveshtan dictionary be file ba indent 4

def add_comment(car_id, username, comment):  # tabe baraye ezafe kardan comment
    data = load_json(comments_file)  # load kardan data comment ha
    
    if "comments" not in data:  # agar key comments vojood nadashte bashe
        data["comments"] = []  # list khali misazim
    
    data["comments"].append({  # ezafe kardan comment jadid
        "car_id": car_id,
        "username": username,
        "comment": comment
    })
    
    save_json(comments_file, data)  # zakhire data jadid
    return True  # payan tabe, comment ezafe shod

def get_comments_by_car(car_id):  # tabe baraye gereftan comment ha bar asas car_id
    data = load_json(comments_file)  # load comment ha
    comments = data.get("comments", [])  # gereftan list comments
    return [c for c in comments if c["car_id"] == car_id]  # filter comment ha bar asas car_id

def get_all_comments():  # tabe baraye gereftan hame comment ha
    data = load_json(comments_file)
    return data.get("comments", [])  # barmigardan list comment ha

def add_reservation(username, car_id, car_name, car_brand):  # tabe baraye ezafe kardan reservation
    data = load_json(reservations_file)  # load data reservations
    
    if "reservations" not in data:  # agar key vojood nadashte bashe
        data["reservations"] = []  # list khali misazim
    
    data["reservations"].append({  # ezafe kardan reservation jadid
        "username": username,
        "car_id": car_id,
        "car_name": car_name,
        "car_brand": car_brand
    })
    
    save_json(reservations_file, data)  # zakhire data jadid
    return True  # payan tabe, reservation ezafe shod

def get_all_reservations():  # tabe baraye gereftan hame reservations
    data = load_json(reservations_file)
    return data.get("reservations", [])  # barmigardan list reservations
