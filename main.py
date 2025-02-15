import os
import telebot
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🔍 Muhit o‘zgaruvchilarini yuklash
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Telegram boti uchun token
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")  # Google API uchun JSON credentials
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")  # Google Sheets ID

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
    creds_dict = json.loads(GOOGLE_CREDENTIALS)  # JSON stringni dictionary ko‘rinishiga o‘tkazish
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    print("✅ Google Sheets bilan muvaffaqiyatli bog‘landik!")
except Exception as e:
    raise ValueError(f"❌ Google Sheets bilan bog‘lanishda xatolik: {e}")

# 🔹 Telegram botni ishga tushirish
bot = telebot.TeleBot(BOT_TOKEN)

# 📩 /start komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! 👋 Men Google Sheets bilan ishlovchi botman!")

# 📩 /add komandasi -> Google Sheetsga ma'lumot qo‘shish
@bot.message_handler(commands=['add'])
def add_data(message):
    try:
        text = message.text.replace("/add", "").strip()
        if not text:
            bot.reply_to(message, "⚠️ Iltimos, qo‘shiladigan matnni ham yuboring.\nMisol: `/add O‘quvchilar ro‘yxati`")
            return
        
        sheet.append_row([text])  # Google Sheetsga qo‘shish
        bot.reply_to(message, f"✅ `{text}` ma'lumoti muvaffaqiyatli qo‘shildi!")
    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik yuz berdi: {e}")

# 🔄 Botni ishga tushirish
print("🚀 Telegram bot ishga tushirildi...")
bot.polling(none_stop=True)
