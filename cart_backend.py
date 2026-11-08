import json  # import library baraye khandan va neveshtan file ha dar format JSON
import os    # import library baraye barresi vojood file ha
from comment_backend import add_reservation  # import tabe add_reservation az backend

cars_file = "cars.json"  # file JSON ke hame khodro ha dar an zakhire mishan
cart_file = "cart.json"  # file JSON baraye cart karbar

def load_json(filename):  # tabe baraye load kardan data az file JSON
    if not os.path.exists(filename):  # agar file vojood nadashte bashe
        return {}  # dictionary khali barmigardanim
    with open(filename, "r") as file:  # khandan file
        return json.load(file)  # load kardan data va barmigardan dictionary

def save_json(filename, data):  # tabe baraye zakhire kardan data dar file JSON
    with open(filename, "w") as file:  # baz kardan file dar mode write
        json.dump(data, file, indent=4)  # neveshtan dictionary be file ba indent 4

def add_to_cart(car_id):  # tabe baraye ezafe kardan yek khodro be cart
    if not os.path.exists(cars_file):  # barresi vojood file cars
        return False  # agar vojood nadashte bashe, False barmigardim

    cars_data = load_json(cars_file)  # load kardan data cars

    car = None  # variable baraye peyda kardan car monaseb
    for c in cars_data["cars"]:  # halghe baraye jostojo dar list cars
        if c["id"] == car_id:  # agar id monaseb bood
            car = c  # assign kardan
            break  # kharej shodan az halghe

    if not car:  # agar car peyda nashod
        return False

    if car["available"] < 1:  # agar car mojood nist
        return False

    if os.path.exists(cart_file):  # agar cart file vojood dasht
        cart_data = load_json(cart_file)  # load data
        if "items" not in cart_data:  # agar items vojood nadashte bashe
            cart_data["items"] = []  # list khali misazim
    else:  # agar cart file vojood nadashte bashe
        cart_data = {"items": []}  # list khali misazim

    found = False  # barresi vojood car dar cart
    for item in cart_data["items"]:
        if item["car_id"] == car_id:
            found = True
            break

    if not found:  # agar car dar cart vojood nadashte bashe
        cart_data["items"].append({  # ezafe kardan car be cart
            "car_id": car_id,
            "name": car["name"],
            "brand": car["brand"],
            "price": car["price"]
        })

    save_json(cart_file, cart_data)  # zakhire cart jadid
    return True  # ezafe shodan movafagh

def get_cart_items():  # tabe baraye gereftan hame item ha dar cart
    if not os.path.exists(cart_file):  # agar cart vojood nadashte bashe
        return []  # list khali barmigardanim

    cart_data = load_json(cart_file)  # load data
    return cart_data.get("items", [])  # barmigardanim list items

def remove_from_cart(car_id):  # tabe baraye hazf kardan yek item az cart
    if not os.path.exists(cart_file):
        return False

    cart_data = load_json(cart_file)
    cart_data["items"] = [item for item in cart_data["items"] if item["car_id"] != car_id]  # hazf item monaseb

    save_json(cart_file, cart_data)  # zakhire cart jadid
    return True

def clear_cart():  # tabe baraye pak kardan kol cart
    if os.path.exists(cart_file):
        os.remove(cart_file)  # hazf file cart

def get_cart_total():  # tabe baraye mohasebe total price cart
    items = get_cart_items()  # gereftan hame items
    total = 0
    for item in items:  # halghe baraye jam kardan price ha
        total += item["price"]
    return total  # barmigardanim total

def reserve_cars(username):  # tabe baraye reserve kardan hame khodro ha dar cart
    items = get_cart_items()  # gereftan hame items

    if not items:  # agar cart khali bashe
        return False, "Cart is empty"

    cars_data = load_json(cars_file)  # load data cars

    for item in items:  # halghe baraye check va reserve kardan
        for car in cars_data["cars"]:
            if car["id"] == item["car_id"]:
                if car["available"] >= 1:  # agar car mojood bood
                    car["available"] -= 1  # kam kardan available
                    car["reserved"] += 1  # ziyad kardan reserved
                    add_reservation(username, car["id"], car["name"], car["brand"])  # farakhani add_reservation
                else:  # agar car mojood nabood
                    return False, f"{car['name']} is no longer available"

    save_json(cars_file, cars_data)  # zakhire data cars jadid
    clear_cart()  # pak kardan cart

    return True, "Reservation successful"  # payan tabe, reserve movafagh
