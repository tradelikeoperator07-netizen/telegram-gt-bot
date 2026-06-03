import json, os, random, asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

BOT_TOKEN = "8264438185:AAEGGRgQ5_FU-ERfoEZU05IPtywuLorU8ss"
CHANNEL_LINK = "https://t.me/+R9YjIH3JprU5MGU1"
USERS_FILE = "users.json"

FUNNEL_DELAYS = [2, 8, 24, 3, 12, 6, 24]

FUNNEL_MESSAGES = [
    ("poster1.jpg", "🔥 Join our VIP group now and get FREE signals today!\n\n👉 Don't miss out!\n🔗 " + CHANNEL_LINK),
    ("poster2.jpg", "📊 Our members made big profits today!\n\n💰 Click below to join now!\n🔗 " + CHANNEL_LINK),
    ("poster3.jpg", "🚀 Free VIP access won't last long!\n\n⚡ Join now!\n🔗 " + CHANNEL_LINK),
    ("poster4.jpg", "💎 VIP members got 10 winning signals today!\n\n✅ Join FREE now!\n🔗 " + CHANNEL_LINK),
    ("poster1.jpg", "🎯 New signals dropping soon!\n\n👇 Join for FREE!\n🔗 " + CHANNEL_LINK),
    ("poster2.jpg", "💸 Our traders are winning daily!\n\n🔥 Limited spots!\n🔗 " + CHANNEL_LINK),
    ("poster3.jpg", "⚡ FREE VIP access today only!\n\n🚀 Join now!\n🔗 " + CHANNEL_LINK),
]

# Main buttons shown with welcome + posters
main_keyboard = [
    [InlineKeyboardButton("🥳 FREE VIP GROUP", url=CHANNEL_LINK)],
    [InlineKeyboardButton("📊 CONTACT OWNER", url="https://t.me/GautamTraderAdmin?text=Hello%20Gautam%20Sir%2C%20I%20am%20interested%20in%20earning%20money%20%F0%9F%92%B0")]
]
main_markup = InlineKeyboardMarkup(main_keyboard)

# Buttons shown with circle video
video_keyboard = [
    [InlineKeyboardButton("💰 WANT FREE $1000?", url="https://t.me/GautamTraderAdmin?text=Gautam%20Sir%2C%20I%20want%20to%20claim%20the%20%241000%20profit.%20Please%20guide%20me%20with%20the%20complete%20process%20to%20get%20started%20%F0%9F%9A%80%F0%9F%92%B8")],
    [InlineKeyboardButton("📉 LOSS RECOVERY", url="https://t.me/GautamTraderAdmin?text=Gautam%20Sir%2C%20I%20am%20in%20loss%20right%20now%20and%20I%20want%20to%20recover%20my%20losses%20with%20proper%20guidance.%20Please%20help%20me%20join%20your%20VIP%20Loss%20Recovery%20Session%20%F0%9F%99%8F%F0%9F%93%88")]
]
video_markup = InlineKeyboardMarkup(video_keyboard)

scheduler = AsyncIOScheduler()


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)


async def send_funnel_message(bot, user_id, step):
    users = load_users()
    uid = str(user_id)
    if uid not in users:
        return
    msg_index = step % len(FUNNEL_MESSAGES)
    image_file, caption = FUNNEL_MESSAGES[msg_index]
    try:
        with open(image_file, "rb") as photo:
            await bot.send_photo(chat_id=user_id, photo=photo, caption=caption, reply_markup=main_markup)
    except Exception as e:
        print(f"Failed to send to {user_id}: {e}")
        return
    next_step = step + 1
    if next_step < len(FUNNEL_DELAYS):
        delay_hours = FUNNEL_DELAYS[next_step]
    else:
        delay_hours = random.randint(3, 24)
    users[uid]["step"] = next_step
    save_users(users)
    run_time = datetime.now() + timedelta(hours=delay_hours)
    scheduler.add_job(send_funnel_message, trigger=DateTrigger(run_date=run_time), args=[bot, user_id, next_step], id=f"funnel_{user_id}_{next_step}", replace_existing=True)
    print(f"Next message for {user_id} in {delay_hours} hours")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)
    users = load_users()
    if uid not in users:
        users[uid] = {"step": 0, "joined": str(datetime.now())}
        save_users(users)

    # 1. Send welcome poster with main buttons
    try:
        with open("poster1.jpg", "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=f"🚀 Welcome {user.first_name} to Gautam GT VIP!\n\n🔥 Get FREE Quotex Signals every day!\n👉 Join our FREE VIP group below 👇",
                reply_markup=main_markup
            )
    except Exception as e:
        print(f"Poster error: {e}")
        await update.message.reply_text(
            f"🚀 Welcome {user.first_name} to Gautam GT VIP!\n\n🔥 Get FREE Quotex Signals every day!\n👉 Join our FREE VIP group below 👇",
            reply_markup=main_markup
        )

    # 2. Wait 5 seconds then send circle video with new buttons
    await asyncio.sleep(5)
    try:
        with open("video.MP4", "rb") as video:
            await update.message.reply_video_note(video=video)
        await update.message.reply_text(
            "👇 Choose your next step:",
            reply_markup=video_markup
        )
    except Exception as e:
        print(f"Video error: {e}")

    # 3. Schedule funnel
    run_time = datetime.now() + timedelta(hours=FUNNEL_DELAYS[0])
    scheduler.add_job(send_funnel_message, trigger=DateTrigger(run_date=run_time), args=[context.bot, user.id, 0], id=f"funnel_{user.id}_0", replace_existing=True)
    print(f"Funnel started for {user.first_name}")


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = " ".join(context.args)
    users = load_users()
    sent = 0
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message)
            sent += 1
        except Exception:
            pass
    await update.message.reply_text(f"Broadcast sent to {sent} users.")


async def channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post
    if not post:
        return
    users = load_users()
    sent = 0
    for user_id in users:
        try:
            await context.bot.copy_message(chat_id=int(user_id), from_chat_id=post.chat.id, message_id=post.message_id, reply_markup=main_markup)
            sent += 1
        except Exception as e:
            print(e)
    print(f"Forwarded to {sent} users")


app = Application.builder().token(BOT_TOKEN).build()
scheduler.start()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.ALL, channel_post))
print("Bot is running...")
app.run_polling()
