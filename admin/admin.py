# admin.py
from aiogram import types, Dispatcher
from config import ADMINS
from database import db, update_user_balance
from aiogram.dispatcher.filters import Command

ADMINS = [5500391037, 2087667844]
# Faqat adminlar uchun tekshiruv
def is_admin(user_id):
    return user_id in ADMINS

# Balans to‘ldirish funksiyasi
async def add_balance_command(message: types.Message):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ Sizga bu buyruqni bajarish mumkin emas.")

    try:
        args = message.text.split()
        if len(args) != 3:
            return await message.answer("❗️ To‘g‘ri format: /add_balance user_id miqdor")

        user_id = int(args[1])
        amount = int(args[2])

        if user_id not in db:
            return await message.answer("❌ Foydalanuvchi topilmadi.")

        update_user_balance(user_id, amount)
        await message.answer(f"✅ Foydalanuvchi {user_id} hisobiga {amount} so‘rov qo‘shildi.")
    except:
        await message.answer("❌ Noto‘g‘ri format. Foydalanish: /add_balance user_id miqdor")

# Foydalanuvchilar ro‘yxati
async def user_list_command(message: types.Message):
    if not is_admin(message.from_user.id):
        return

    text = "📋 Foydalanuvchilar ro‘yxati:\n"
    for user_id, info in db.items():
        text += f"ID: {user_id} | Ism: {info['name']} | Balans: {info['balance']}\n"
    await message.answer(text if text else "Hech qanday foydalanuvchi topilmadi.")

# Admin buyruqlarini ro‘yxatdan o‘tkazamiz
def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(add_balance_command, Command("add_balance"))
    dp.register_message_handler(user_list_command, Command("userlist"))
