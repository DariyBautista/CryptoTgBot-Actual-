import os, json
from config import DATA_FILE

user_data = {}

def load_data():
    global user_data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
                user_data = {int(k): v for k, v in raw.items()}
        except (json.JSONDecodeError, ValueError):
            print("Error: Corrupted JSON file. Starting with empty data.")
            user_data = {}
    else:
        user_data = {}


def save_data():
    # print("💾 save_data():", DATA_FILE, "with", user_data)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in user_data.items()}, f, ensure_ascii=False, indent=2)
