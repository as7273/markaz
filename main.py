import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# 🔹 Google Sheets API uchun sozlash
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "service_account.json"  # Railway'ga yuklangan fayl
credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(os.environ["SERVICE_ACCOUNT_JSON"]), SCOPES)
client = gspread.authorize(credentials)

# 🔹 Google Sheets hujjatini ochish
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")  # Railway'dan olish
sheet = client.open_by_key(SPREADSHEET_ID).sheet1  # 1-qatordagi sahifa

# 🔹 Telegram bot tokeni
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Railway'dan olish
bot = telebot.TeleBot(BOT_TOKEN)

# 🔹 Start komandasi
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Salom! Farzandingizning test natijalarini ko‘rish uchun telefon raqamingizni yuboring.")

# 🔹 Telefon raqam orqali natija chiqarish
@bot.message_handler(content_types=["contact"])
def get_results(message):
    phone_number = message.contact.phone_number
    try:
        records = sheet.get_all_records()
        for row in records:
            if str(row["Telefon"]) == phone_number:
                result = f"📊 Test natijalari:\n\nFan: {row['Fan']}\nBall: {row['Ball']}%"
                bot.send_message(message.chat.id, result)
                return
        bot.send_message(message.chat.id, "⚠️ Sizning telefon raqamingiz bo‘yicha natija topilmadi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik yuz berdi: {e}")

# 🔹 Botni ishga tushirish
bot.polling()
