import os
from dotenv import load_dotenv

load_dotenv()

# print(os.environ.get('BOT_TOKEN'))  # должно напечатать ваш токен
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env файле")