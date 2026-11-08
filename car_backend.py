# car_backend.py
import json  # import library baraye khandan va neveshtan file ha dar format JSON
import os    # import library baraye barresi vojood file ha

cars_file = "cars.json"  # esm file ke hame khodro ha dar an zakhire mishan

def add_car(name, brand, year, price, available):  # tabe baraye ezafe kardan yek khodro jadid
    if not os.path.exists(cars_file):  # barresi vojood file, agar vojood nadashte bashe
        data = {"cars": [], "last_id": 0}  # misazim dictionary khali baraye khodro ha va last_id
    else:
        with open(cars_file, "r") as file:  # agar file vojood dasht, an ra mikhanim
            data = json.load(file)  # load kardan data az file be form dictionary
    
    if "last_id" not in data:  # barresi vojood klid last_id
        data["last_id"] = 0  # agar vojood nadashte bashe, 0 migzarim

    data["last_id"] += 1  # har khodro jadid, id jadid migire

    new_car = {  # tarif dictionary baraye khodro jadid
        "id": data["last_id"],
        "name": name,
        "brand": brand,
        "year": year,
        "price": price,
        "available": available,  # tedad mojood
        "reserved": 0  # tedad reserved avalieh 0
    }
    data["cars"].append(new_car)  # ezafe kardan khodro jadid be list

    with open(cars_file, "w") as file:  # zakhire kardan data dar file JSON
        json.dump(data, file, indent=4)

def get_all_cars():  # tabe baraye gereftan hame khodro ha
    if not os.path.exists(cars_file):  # agar file vojood nadashte bashe
        return []  # list khali barmigardanim
    with open(cars_file, "r") as file:  # khandan file
        data = json.load(file)  # load kardan data
        return data.get("cars", [])  # barmigardanim list khodro ha, agar vojood nadashte bashe list khali

def get_car_by_id(car_id):  # tabe baraye gereftan khodro ba id moshakhas
    cars = get_all_cars()  # gereftan hame khodro ha
    for car in cars:  # halghe baraye jostojo
        if car["id"] == car_id:  # agar id monaseb bood
            return car  # khodro ra barmigardanim
    return None  # agar nafrid kardim, None barmigardanim

def edit_car(car_id, name, brand, year, price, available):  # tabe baraye edit kardan khodro
    if not os.path.exists(cars_file):  # agar file vojood nadashte bashe
        return False

    with open(cars_file, "r") as file:  # khandan file
        data = json.load(file)

    for car in data["cars"]:  # halghe baraye peyda kardan khodro ba id
        if car["id"] == car_id:
            car["name"] = name
            car["brand"] = brand
            car["year"] = year
            car["price"] = price
            car["available"] = available
            break  # pas az peyda kardan, halghe ro mikonim

    with open(cars_file, "w") as file:  # zakhire kardan data jadid dar file
        json.dump(data, file, indent=4)
    return True  # agar edit shod, True midim

def delete_car(car_id):  # tabe baraye hazf kardan khodro ba id
    if not os.path.exists(cars_file):  # agar file vojood nadashte bashe
        return False

    with open(cars_file, "r") as file:  # khandan file
        data = json.load(file)

    data["cars"] = [car for car in data["cars"] if car["id"] != car_id]  # hazf khodro ha ke id anha monaseb nist

    with open(cars_file, "w") as file:  # zakhire data jadid
        json.dump(data, file, indent=4)
    return True  # agar delete shod, True midim
