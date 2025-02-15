




import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# GOOGLE_CREDENTIALS ni olish
google_creds = os.getenv("GOOGLE_CREDENTIALS")

if not google_creds:
    raise ValueError("❌ GOOGLE_CREDENTIALS yo‘q! Railway'dagi muhit o‘zgaruvchisini tekshiring.")

try:
    creds_json = json.loads(google_creds)
except json.JSONDecodeError:
    raise ValueError("❌ GOOGLE_CREDENTIALS noto‘g‘ri JSON formatida saqlangan.")

# Google API uchun autentifikatsiya qilish
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

print("✅ Google Sheets bilan muvaffaqiyatli bog‘landik!")







import os

google_creds = os.getenv("GOOGLE_CREDENTIALS")

if google_creds is None:
    raise ValueError("❌ GOOGLE_CREDENTIALS yo‘q! Railway'da muhit o‘zgaruvchisini to‘g‘ri o‘rnating.")
else:
    print("✅ GOOGLE_CREDENTIALS mavjud!")




import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# GOOGLE_CREDENTIALS ni tekshirish
creds_json_str = os.getenv("GOOGLE_CREDENTIALS")

if not creds_json_str:
    raise ValueError("❌ GOOGLE_CREDENTIALS topilmadi! Railway'dagi muhit o‘zgaruvchisini tekshiring.")

try:
    creds_json = json.loads(creds_json_str)
except json.JSONDecodeError:
    raise ValueError("❌ GOOGLE_CREDENTIALS JSON formatida noto‘g‘ri saqlangan. Railway'dagi ma’lumotni tekshiring.")

# Google Sheets API uchun autentifikatsiya qilish
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

print("✅ Google Sheets bilan muvaffaqiyatli bog‘landik!")







import os
import json
import gspread
import telebot
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request
import os


# 📌 Flask ilovasini yaratamiz (Railway uchun kerak)
app = Flask(__name__)

# 📌 Railway environment variables orqali API kalitlarni yuklash
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# 📌 Google Sheets'ga ulanish
creds_json = json.loads(os.getenv("GOOGLE_CREDENTIALS"))  # Railway'dan JSON yuklash
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, SCOPES)
client = gspread.authorize(credentials)

# 📌 Google Sheets sahifasini ochamiz
sheet = client.open_by_key(SPREADSHEET_ID).sheet1  # Birinchi qatordagi sahifa

# 📌 Telegram botini ishga tushiramiz
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 📌 Start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salom! Bu bot Google Sheets bilan ishlaydi.")

# 📌 Google Sheets'ga yozish funksiyasi
@bot.message_handler(func=lambda message: True)
def save_to_sheet(message):
    try:
        text = message.text
        user = message.chat.username or message.chat.first_name
        sheet.append_row([user, text])  # Foydalanuvchi nomi va xabarini saqlash
        bot.send_message(message.chat.id, "Xabaringiz Google Sheets'ga saqlandi!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik: {e}")

# 📌 Railway uchun webhook sozlash
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# 📌 Flask serverni ishga tushiramiz
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# GOOGLE_CREDENTIALS o'zgaruvchisini ekranga chiqarish
print("GOOGLE_CREDENTIALS:", os.getenv("GOOGLE_CREDENTIALS"))
