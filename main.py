import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
MAX_USERS = 50
ENTRY_CODE = "ARW-982341"
ROOM_LINK = "https://example.com"
IMAGE_URL = "https://i.ibb.co/PcFZRLk/freefire.jpg"
CONTACT_INFO = "📞 8219787394\n📲 Telegram: @arvind_k_82"

def get_user_count():
    with open("user_count.json", "r") as f:
        return json.load(f)["count"]

def increment_user_count():
    with open("user_count.json", "r") as f:
        data = json.load(f)
    data["count"] += 1
    with open("user_count.json", "w") as f:
        json.dump(data, f)

def reset_user_count():
    with open("user_count.json", "w") as f:
        json.dump({"count": 0}, f)

def is_admin(user_id):
    with open("admin.json", "r") as f:
        return user_id in json.load(f)["admins"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    print("🆔 Telegram ID:", user_id)

    count = get_user_count()
    if count >= MAX_USERS:
        await context.bot.send_message(chat_id=chat_id, text="🚫 Booking Full! Wait for next round.")
    else:
        increment_user_count()
        message = f"""✅ Payment Confirmed!

🎮 Code: `{ENTRY_CODE}`
🔗 Room Link: {ROOM_LINK}

📱 *Contact Support:*
{CONTACT_INFO}"""
        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        await context.bot.send_photo(chat_id=chat_id, photo=IMAGE_URL, caption="🖼️ Your UID QR")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_admin(user_id):
        reset_user_count()
        await update.message.reply_text("✅ Reset done.")
    else:
        await update.message.reply_text("⛔ Not authorized.")

if __name__ == "__main__":
    print("🤖 Ar Win Bot is running...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.run_polling()
