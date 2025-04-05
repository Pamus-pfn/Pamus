# database.py
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os

DB_URL = os.getenv("DATABASE_URL")  # Railway .env dan keladi

# PostgreSQLga ulanish
conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
cursor = conn.cursor()

# Jadval yaratish
def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            name TEXT,
            balance INTEGER DEFAULT 0,
            spent INTEGER DEFAULT 0,
            registered_at TIMESTAMP
        )
    """)
    conn.commit()

# Yangi foydalanuvchi qo‘shish
def register_user(user_id, name):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO users (user_id, name, registered_at)
            VALUES (%s, %s, %s)
        """, (user_id, name, datetime.now()))
        conn.commit()

# Balans qo‘shish
def update_user_balance(user_id, amount):
    cursor.execute("""
        UPDATE users SET balance = balance + %s WHERE user_id = %s
    """, (amount, user_id))
    conn.commit()

# Balansdan yechish
def decrease_balance(user_id, amount):
    cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
    data = cursor.fetchone()
    if data and data["balance"] >= amount:
        cursor.execute("""
            UPDATE users
            SET balance = balance - %s, spent = spent + %s
            WHERE user_id = %s
        """, (amount, amount, user_id))
        conn.commit()
        return True
    return False

# Foydalanuvchi haqida info
def get_user_info(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    return cursor.fetchone()