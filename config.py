# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # .env fayldan o‘qish uchun

# Bot tokeni
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Gemini AI API kaliti
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Adminlar ID ro‘yxati
ADMINS = [5500391037, 2087667844]