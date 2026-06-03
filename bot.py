import json, os, random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

BOT_TOKEN = "8264438185:AAEGGRgQ5_FU-ERfoEZU05IPtywuLorU8ss"
CHANNEL_LINK = "https://t.me/+R9YjIH3JprU5MGU1"
USERS_FILE = "users.json"

# Funnel delays in hours
FUNNEL_DELAYS = [2, 8, 24, 3, 12, 6, 24]

# Posters and captions
FUNNEL_MESSAGES = [
    ("poster1.jpg", "🔥 Special Offer! Join our VIP group now and get FREE signals today!\n\n👉 Don't miss out!\n🔗 " + CHANNEL_LINK),
    ("poster2.jpg", "📊 Our members made big profits today! Join us FREE!\n\n💰 Click below to join now!\n🔗 " + CHANNEL_LINK),
    ("poster3.jpg", "🚀 Last chance! Free VIP access won't last long!\n\n⚡ Join now before it closes!\n🔗 " + CHANNEL_LINK),
    ("poster4.jpg", "💎 VIP members got 10 winning signals today!\n\n✅ Join FREE now!\n🔗 " + CHANNEL_LINK),
    ("poster1.jpg", "🎯 New signals dropping soon! Are you in the VIP group?\n\n👇 Join for FREE!\n🔗 " + CHANNEL_LINK),
    ("poster2.jpg", "💸 Our traders are winning daily! Join our FREE VIP group!\n\n🔥 Limited spots!\n🔗 " + CHANNEL_LINK),
    ("poster3.jpg", "⚡ TODAY only - FREE VIP access! Don't wait!\n\n🚀 Join now!\n🔗 " + CHANNEL_LINK),
]

keyboard = [
    [InlineKeyboardButton("🥳 FREE VIP GROUP", url=CHANNEL_LINK)],
    [InlineKeyboardButton("📊 CONTACT OWNER", url="https://t.me/GautamTraderAdmin?text=Hello%20Gautam%20Sir%2C%20I%20am%20interested%20in%20earning%20money%20%F0%9F%92%B0")]
]
reply_markup = InlineKeyboardMarkup(keyboard)

scheduler = AsyncIOScheduler()

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

async def send_funnel_message(bot, user_id: int, step: int):
    users = load_users()
    uid = str(user_id)
    if uid not in users:
        return

    msg_index = step % len(FUNNEL_MESSAGES)
    image_file, caption = FUNNEL_MESSAGES[msg_index]

    try:
        with open(image_file, "rb") as photo:
            await bot.send_photo(
                chat_id=user_id,
                photo=photo,
                caption=caption,
                reply_markup=reply_markup
            )
    except Exception as e:
        print(f"Failed to send funnel msg to {user_id}: {e}")
        return

    next_step = step + 1
    if next_step < len(FUNNEL_DELAYS):
        delay_hours = FUNNEL_DELAYS[next_step]
    else:
