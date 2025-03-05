import json
import os


def show_expenses():
    if not os.path.isfile('data.json'):
        with open('data.json', 'w') as f:
            json.dump([], f)
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data


def add_expenses(data):
    with open("data.json", "w") as f:
        json.dump(data, f)