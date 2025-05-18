import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CMC_API_KEY    = os.environ.get("CMC_API_KEY")
import os
BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "user_data.json")
