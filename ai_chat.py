# ai_chat.py
import aiohttp
from config import GEMINI_API_KEY

# Gemini API manzili
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

headers = {
    "Content-Type": "application/json"
}

# AI javob funksiyasi
async def get_ai_response(question: str) -> str:
    async with aiohttp.ClientSession() as session:
        params = {"key": GEMINI_API_KEY}
        data = {
            "contents": [{
                "parts": [{"text": question}]
            }]
        }

        async with session.post(GEMINI_API_URL, headers=headers, params=params, json=data) as response:
            if response.status == 200:
                result = await response.json()
                try:
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError):
                    return "❗ AI javob bera olmadi. Keyinroq urinib ko‘ring."
            else:
                return "❗ Xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko‘ring."