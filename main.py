from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN, ADMINS
from database import db, create_user, get_user, update_user_balance
from ai_chat import get_ai_response
from admin import register_admin_handlers

import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- START: Menu Buttonlar
menu_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
menu_buttons.row(
    KeyboardButton("1️⃣ Savol berish"),
    KeyboardButton("2️⃣ Psixologik Test")
)
menu_buttons.row(
    KeyboardButton("💎 Premium"),
    KeyboardButton("📞 Bog‘lanish")
)
menu_buttons.add(KeyboardButton("📊 Hisobim"))
# --- END: Menu Buttonlar

# --- START: Foydalanuvchi boshlaganda
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    create_user(message.from_user)

    await message.answer(
        "🧠 <b>PsixologTop - AiChat</b>\n\n"
        "Sizning sun'iy intellekt yordamchingiz! 🌟\n\n"
        "📌 <b>O'zbek tilida istalgan psixologik savollaringizni quyidagi formatlarda yuboring:</b>\n"
        "✅ Matn – yozma ravishda savolingizni yuboring\n"
        "🎙 Audio – ovozli xabar yuboring\n"
        "📷 Rasm – yuz ifodalari orqali tahlil (tez orada!)\n\n"
        "✨ <b>PsixologTop - AiChat</b> sizga tezkor va aniq javoblar beradi!\n\n"
        "📌 <b>Qo'shimcha funksiyalar:</b>\n"
        "🔹 Stress va depressiya testlari\n"
        "🔹 Shaxsiy maslahatlar va tavsiyalar\n"
        "🔹 Motivatsion xabarlar va mashqlar\n"
        "🔹 Meditatsiya va ongni tinchlantirish texnikalari\n\n"
        "💎 <b>Premium xizmatini faollashtiring!</b>\n"
        "Botdan <b>1 marta BEPUL</b> foydalanishingiz mumkin! Shundan so‘ng, davom etish uchun Premium xizmatga o'tishingiz kerak\n\n"
        "🚀 Premium xizmatlardan foydalanish uchun pastdagi <b>\"Premium\"</b> tugmasini bosing!\n\n"
        "🆘 Savollaringiz bo'lsa yoki qo'shimcha yordam kerak bo'lsa, pastdagi <b>\"Bog‘lanish\"</b> tugmasini bosing!\n\n"
        "💬 Savollaringizni yuboring… 👇",
        parse_mode="HTML",
        reply_markup=menu_buttons
    )
# --- END

# --- Savol berish
@dp.message_handler(Text(equals="1️⃣ Savol berish"))
async def ask_question_handler(message: types.Message):
    user = get_user(message.from_user.id)
    if user["free_question"] == 0 and user["balance"] <= 0:
        await message.answer("❌ Sizning bepul savolingiz ishlatilgan.\nPremium xizmatlarga o‘ting.")
    else:
        await message.answer("Savolingizni yozing:")
        await dp.current_state(user=message.from_user.id).set_state("waiting_for_question")

@dp.message_handler(state="waiting_for_question")
async def answer_question(message: types.Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    answer = get_ai_response(message.text)
    await message.answer(answer)

    if user["free_question"] > 0:
        db[user_id]["free_question"] -= 1
    else:
        db[user_id]["balance"] -= 1

    await dp.current_state(user=message.from_user.id).finish()

# --- Psixologik test (namuna)
@dp.message_handler(Text(equals="2️⃣ Psixologik Test"))
async def test_handler(message: types.Message):
    await message.answer("Testlar tayyorlanmoqda. Tez orada mavjud bo‘ladi.")

# --- Premium xizmat
@dp.message_handler(Text(equals="💎 Premium"))
async def premium_handler(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🚀 Start tarif – 50k", callback_data="start_tarif"),
        InlineKeyboardButton("⚡ Medium tarif – 100k", callback_data="medium_tarif"),
        InlineKeyboardButton("✨ Best tarif – 150k", callback_data="best_tarif")
    )
    await message.answer(
        "💎 Premium Xizmatlar\n"
        "Quyidagi tariflardan birini tanlang:",
        reply_markup=markup
    )

@dp.callback_query_handler(Text(startswith="start_tarif"))
async def start_tarif_handler(call: types.CallbackQuery):
    await call.message.answer(
        "🚀 START TARIF – 1 soatlik foydalanish\n"
        "Narxi: 50,000 so‘m\n"
        "To‘lov uchun: @Psixolog_admin1"
    )
    await call.answer()

@dp.callback_query_handler(Text(startswith="medium_tarif"))
async def medium_tarif_handler(call: types.CallbackQuery):
    await call.message.answer(
        "⚡ MEDIUM TARIF – 3 soatlik foydalanish\n"
        "Narxi: 100,000 so‘m\n"
        "To‘lov uchun: @Psixolog_admin1"
    )
    await call.answer()

@dp.callback_query_handler(Text(startswith="best_tarif"))
async def best_tarif_handler(call: types.CallbackQuery):
    await call.message.answer(
        "✨ BEST TARIF – 5 soatlik foydalanish\n"
        "Narxi: 150,000 so‘m\n"
        "To‘lov uchun: @Psixolog_admin1"
    )
    await call.answer()

# --- Bog‘lanish
@dp.message_handler(Text(equals="📞 Bog‘lanish"))
async def contact_handler(message: types.Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Admin bilan bog‘lanish", url="https://t.me/Psixolog_admin1"))
    await message.answer("📞 Savollaringiz bo‘lsa admin bilan bog‘laning:", reply_markup=markup)

# --- Hisobim
@dp.message_handler(Text(equals="📊 Hisobim"))
async def account_handler(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(
        f"🏛 Sizning hisobingiz:\n"
        f"Mijoz: {message.from_user.full_name}\n"
        f"ID: {message.from_user.id}\n"
        f"Hisob: {user['balance']} so‘rov\n"
        f"Sarflagan: {user['used']} so‘m\n"
        f"Status: {'📝 Oddiy' if user['balance'] == 0 else '🌟 Premium'}\n"
        f"⏰ So‘nggi kirish: {user['last_seen']}"
    )

# --- Admin handlerlarni ro‘yxatdan o‘tkazamiz
register_admin_handlers(dp)

# --- Botni ishga tushirish
if name == 'main':
    print("Bot ishga tushdi...")
    from database import load_db
    load_db()
    executor.start_polling(dp, skip_updates=True)   