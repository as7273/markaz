import os
import telebot
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ✅ Muhit o‘zgaruvchilarini yuklash
BOT_TOKEN = os.getenv("BOT_TOKEN")  # TO‘G‘RI NOM
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# 🔎 Muhit o‘zgaruvchilarini tekshirish
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi! Railway'dagi muhit o‘zgaruvchisini tekshiring.")

if not GOOGLE_CREDENTIALS:
    raise ValueError("❌ GOOGLE_CREDENTIALS topilmadi! Railway'dagi muhit o‘zgaruvchisini tekshiring.")

if not SPREADSHEET_ID:
    raise ValueError("❌ SPREADSHEET_ID topilmadi! Railway'dagi muhit o‘zgaruvchisini tekshiring.")

print("✅ BOT_TOKEN muvaffaqiyatli yuklandi!")
print("🔍 Railway'dan GOOGLE_CREDENTIALS ni tekshiryapmiz...")

# 🔐 Google Sheets bilan bog‘lanish
try:
    creds_dict = json.loads(GOOGLE_CREDENTIALS)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    print("✅ Google Sheets bilan muvaffaqiyatli bog‘landik!")
except Exception as e:
    raise ValueError(f"❌ Google Sheets bilan bog‘lanishda xatolik: {e}")

# 🔹 Telegram botni ishga tushirish
bot = telebot.TeleBot(BOT_TOKEN)  # TO‘G‘RI NOM ISHLATILDI!

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! 👋 Men Google Sheets bilan ishlovchi botman!")

print("🚀 Telegram bot ishga tushirildi...")
bot.polling(none_stop=True)
