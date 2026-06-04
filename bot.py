import json, os, random, asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ChatMemberHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

BOT_TOKEN = "8264438185:AAEGGRgQ5_FU-ERfoEZU05IPtywuLorU8ss"
CHANNEL_LINK = "https://t.me/+R9YjIH3JprU5MGU1"
USERS_FILE = "users.json"

FUNNEL_DELAYS = [2, 8, 24, 3, 12, 6, 24]

# ── Inline Keyboards ──────────────────────────────────────────────
poster1_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔴 FREE VIP GROUP 📈", url="https://t.me/+R9YjIH3JprU5MGU1")],
    [InlineKeyboardButton("🔵 JOIN LOSS RECOVERY 🎯", url="https://t.me/GautamTraderAdmin?text=Gautam%20Sir%2C%20I%20am%20in%20loss%20right%20now%20and%20I%20want%20to%20recover%20my%20losses%20with%20proper%20guidance.%20Please%20help%20me%20join%20your%20VIP%20Loss%20Recovery%20Session%20%F0%9F%99%8F%F0%9F%93%88.")],
    [InlineKeyboardButton("🟢 CONTACT OWNER 🤝", url="https://t.me/GautamTraderAdmin?text=Gautam%20Sir%2C%20I%20Want%20To%20Build%20A%20Lifestyle%20Like%20Yours.%20Please%20Guide%20Me%20On%20The%20Process%20To%20Join%20Your%20VIP.")]
])

poster2_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("🥳 Join Free VIP", url="https://t.me/+R9YjIH3JprU5MGU1")],
    [InlineKeyboardButton("🆕 NEW IN TRADING?", url="https://t.me/GautamTraderAdmin?text=Gautam%20Sir%2C%20I%20Want%20To%20Build%20A%20Lifestyle%20Like%20Yours.%20Please%20Guide%20Me%20On%20The%20Process%20To%20Join%20Your%20VIP.")]
])

poster3_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("✅ JOIN NOW", url="https://t.me/+R9YjIH3JprU5MGU1")]
])

video_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("💰 WANT FREE 1000$?", url="https://t.me/GautamTraderAdmin?text=Gautam%20Sir%2C%20I%20want%20to%20claim%20the%20%241000%20profit.%20Please%20guide%20me%20with%20the%20complete%20process%20to%20get%20started%20%F0%9F%9A%80%F0%9F%92%B8")],
    [InlineKeyboardButton("📉 LOSS RECOVERY", url="https://t.me/GautamTraderAdmin?text=Gautam%20Sir%2C%20I%20am%20in%20loss%20right%20now%20and%20I%20want%20to%20recover%20my%20losses%20with%20proper%20guidance.%20Please%20help%20me%20join%20your%20VIP%20Loss%20Recovery%20Session%20%F0%9F%99%8F%F0%9F%93%88")]
])

giveaway_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("🆕 NEW IN TRADING?", url="https://t.me/GautamTraderAdmin?text=Gautam%20Sir%2C%20I%20Want%20To%20Build%20A%20Lifestyle%20Like%20Yours.%20Please%20Guide%20Me%20On%20The%20Process%20To%20Join%20Your%20VIP.")],
    [InlineKeyboardButton("📉 LOSS RECOVERY", url="https://t.me/GautamTraderAdmin?text=Gautam%20Sir%2C%20I%20am%20in%20loss%20right%20now%20and%20I%20want%20to%20recover%20my%20losses%20with%20proper%20guidance.%20Please%20help%20me%20join%20your%20VIP%20Loss%20Recovery%20Session%20%F0%9F%99%8F%F0%9F%93%88")]
])

poster5_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("💰 WANT FREE 1000$?", url="https://t.me/GautamTraderAdmin?text=Gautam%20Sir%2C%20I%20want%20to%20claim%20the%20%241000%20profit.%20Please%20guide%20me%20with%20the%20complete%20process%20to%20get%20started%20%F0%9F%9A%80%F0%9F%92%B8")],
    [InlineKeyboardButton("📉 LOSS RECOVERY", url="https://t.me/GautamTraderAdmin?text=Gautam%20Sir%2C%20I%20am%20in%20loss%20right%20now%20and%20I%20want%20to%20recover%20my%20losses%20with%20proper%20guidance.%20Please%20help%20me%20join%20your%20VIP%20Loss%20Recovery%20Session%20%F0%9F%99%8F%F0%9F%93%88")]
])

withdrawal_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("🆕 NEW IN TRADING?", url="https://t.me/GautamTraderAdmin?text=Gautam%20Sir%2C%20I%20Want%20To%20Build%20A%20Lifestyle%20Like%20Yours.%20Please%20Guide%20Me%20On%20The%20Process%20To%20Join%20Your%20VIP.")],
    [InlineKeyboardButton("📉 LOSS RECOVERY", url="https://t.me/GautamTraderAdmin?text=Gautam%20Sir%2C%20I%20am%20in%20loss%20right%20now%20and%20I%20want%20to%20recover%20my%20losses%20with%20proper%20guidance.%20Please%20help%20me%20join%20your%20VIP%20Loss%20Recovery%20Session%20%F0%9F%99%8F%F0%9F%93%88.")]
])

# ── Captions ─────────────────────────────────────────────────────
POSTER1_CAPTION = """<b>🪙 Our Public session Starting In 30 Min Later Don't Miss This Opportunity 👇👇 If You Want To Earn Money 💵

💛 Join My Channel ➡️ Below &amp; Start Earning Money 🤩</b>"""

POSTER2_CAPTION = """<b>🚨 To Continue, Please Join Our Official Channel 🌟 GAUTAM GT ✅

━━━━━━━━━━━━━━━━━━━━━━
🌟 Benefits To Join Channel ⚠️
━━━━━━━━━━━━━━━━━━━━━━

▶️ 95% Accuracy Trades 📈
▶️ Personal LOSS Recovery 📁
▶️ DAILY BUG TOURNAMENT 📊
▶️ Free 10–15 SIGNALS 🚀
▶️ Full COPY-TRADING Access 🛸
▶️ AI Trading HACKBOT 🤖

━━━━━━━━━━━━━━━━━━━━━━
🛸 JOIN FREE VIP GROUP CLICK 👇</b>"""

POSTER3_CAPTION = """<b>🔥📊 Want 10 FREE NON MTG BUG Pocket Signals ?

👉 Click on JOIN CHANNEL now! And you will get FREE 10 Pocket SIGNALS

🔗 LINK : https://t.me/+R9YjIH3JprU5MGU1</b>"""

GIVEAWAY_CAPTION = """<b>💸 These are the results of the trading session of the Telegram community members!!!

⚡️ Congratulations 🤑 to everyone who traded with me today and earned! If you are not making money with us yet, then subscribe to my Telegram channel!

▪️ Link : https://t.me/+R9YjIH3JprU5MGU1</b>"""

POSTER5_CAPTION = """<b>Placed $11,000 Withdrawal IN INR - ₹10,00,000 Money On the Way 💸</b>"""

WITHDRAWAL_CAPTION = """<b>Received $11,000 Withdrawal ✅

Yes, 📈 $11,000 Dollar 💸 (₹10,00,000 in INR) straight cash out — trading se REAL MONEY bahar aa raha hai, sirf balance dikha ne ka game nahi 🚫💳

Now tell me… Tum logon ka profit sirf screenshot tak limited rahega ya withdrawal tak? 🧠🔥</b>"""

# ── Funnel Messages ───────────────────────────────────────────────
FUNNEL_MESSAGES = [
    ("poster1.jpg", POSTER1_CAPTION, poster1_markup),
    ("poster3.jpg", POSTER3_CAPTION, poster3_markup),
    ("poster2.jpg", POSTER2_CAPTION, poster2_markup),
    ("poster1.jpg", POSTER1_CAPTION, poster1_markup),
    ("poster3.jpg", POSTER3_CAPTION, poster3_markup),
    ("poster2.jpg", POSTER2_CAPTION, poster2_markup),
    ("poster1.jpg", POSTER1_CAPTION, poster1_markup),
]

scheduler = AsyncIOScheduler()


# ── Helpers ───────────────────────────────────────────────────────
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)


# ── Withdrawal sender ─────────────────────────────────────────────
async def send_withdrawal(bot, user_id):
    try:
        with open("WITHDRAWL1.jpg", "rb") as w1, open("WITHDRAWL2.jpg", "rb") as w2:
            await bot.send_media_group(
                chat_id=user_id,
                media=[
                    InputMediaPhoto(w1),
                    InputMediaPhoto(w2, caption=WITHDRAWAL_CAPTION, parse_mode="HTML"),
                ]
            )
        await bot.send_message(
            chat_id=user_id,
            text="👇 Choose your next step:",
            reply_markup=withdrawal_markup,
            disable_web_page_preview=True
        )
        print(f"Withdrawal sent to {user_id}")
    except Exception as e:
        print(f"Withdrawal error for {user_id}: {e}")


# ── Poster5 sender ────────────────────────────────────────────────
async def send_poster5(bot, user_id):
    try:
        with open("poster5.jpg", "rb") as photo:
            await bot.send_photo(
                chat_id=user_id,
                photo=photo,
                caption=POSTER5_CAPTION,
                reply_markup=poster5_markup,
                parse_mode="HTML"
            )
        print(f"Poster5 sent to {user_id}")

        # ✅ NORMAL: 55 minutes after poster5
        scheduler.add_job(
            send_withdrawal,
            trigger=DateTrigger(run_date=datetime.now() + timedelta(minutes=55)),
            args=[bot, user_id],
            id=f"withdrawal_{user_id}",
            replace_existing=True
        )
        print(f"Withdrawal scheduled for {user_id} in 55 minutes")
    except Exception as e:
        print(f"Poster5 error for {user_id}: {e}")


# ── Giveaway sender ───────────────────────────────────────────────
async def send_giveaway(bot, user_id):
    try:
        with open("IPHONE1.jpg", "rb") as p1, open("IPHONE2.jpg", "rb") as p2:
            await bot.send_media_group(
                chat_id=user_id,
                media=[
                    InputMediaPhoto(p1),
                    InputMediaPhoto(p2, caption=GIVEAWAY_CAPTION, parse_mode="HTML"),
                ]
            )
        await bot.send_message(
            chat_id=user_id,
            text="👇 Choose your next step:",
            reply_markup=giveaway_markup,
            disable_web_page_preview=True
        )
        print(f"Giveaway sent to {user_id}")

        # ✅ NORMAL: 30 minutes after giveaway
        scheduler.add_job(
            send_poster5,
            trigger=DateTrigger(run_date=datetime.now() + timedelta(minutes=30)),
            args=[bot, user_id],
            id=f"poster5_{user_id}",
            replace_existing=True
        )
        print(f"Poster5 scheduled for {user_id} in 30 minutes")

    except Exception as e:
        print(f"Giveaway error for {user_id}: {e}")


# ── Funnel sender ─────────────────────────────────────────────────
async def send_funnel_message(bot, user_id, step):
    users = load_users()
    uid = str(user_id)
    if uid not in users:
        return

    msg_index = step % len(FUNNEL_MESSAGES)
    image_file, caption, markup = FUNNEL_MESSAGES[msg_index]

    try:
        with open(image_file, "rb") as photo:
            await bot.send_photo(chat_id=user_id, photo=photo, caption=caption, reply_markup=markup, parse_mode="HTML")
    except Exception as e:
        print(f"Failed to send funnel message to {user_id}: {e}")
        return

    next_step = step + 1
    delay_hours = FUNNEL_DELAYS[next_step] if next_step < len(FUNNEL_DELAYS) else random.randint(3, 24)

    users[uid]["step"] = next_step
    save_users(users)

    run_time = datetime.now() + timedelta(hours=delay_hours)
    scheduler.add_job(
        send_funnel_message,
        trigger=DateTrigger(run_date=run_time),
        args=[bot, user_id, next_step],
        id=f"funnel_{user_id}_{next_step}",
        replace_existing=True
    )
    print(f"Next funnel message for {user_id} in {delay_hours} hours (step {next_step})")


# ── /start handler ────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)

    users = load_users()
    if uid not in users:
        users[uid] = {"step": 0, "joined": str(datetime.now())}
        save_users(users)

    # 1. Send poster2 as welcome
    try:
        with open("poster2.jpg", "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=POSTER2_CAPTION, reply_markup=poster2_markup, parse_mode="HTML")
    except Exception as e:
        print(f"Poster error: {e}")
        await update.message.reply_text(POSTER2_CAPTION, reply_markup=poster2_markup, parse_mode="HTML")

    # 2. Wait 5 seconds then send circle video + buttons
    await asyncio.sleep(5)
    try:
        with open("video.MP4", "rb") as video:
            await update.message.reply_video_note(video_note=video)
        await update.message.reply_text("👇 Choose your next step:", reply_markup=video_markup)
    except Exception as e:
        print(f"Video error: {e}")
        await update.message.reply_text("👇 Choose your next step:", reply_markup=video_markup)

    # 3. ✅ NORMAL: Giveaway after 15 minutes
    scheduler.add_job(
        send_giveaway,
        trigger=DateTrigger(run_date=datetime.now() + timedelta(minutes=15)),
        args=[context.bot, user.id],
        id=f"giveaway_{user.id}",
        replace_existing=True
    )

    # 4. Schedule funnel starting after 2 hours
    scheduler.add_job(
        send_funnel_message,
        trigger=DateTrigger(run_date=datetime.now() + timedelta(hours=FUNNEL_DELAYS[0])),
        args=[context.bot, user.id, 0],
        id=f"funnel_{user.id}_0",
        replace_existing=True
    )

    print(f"Funnel + Giveaway scheduled for {user.first_name}")


# ── /broadcast handler ────────────────────────────────────────────
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
    await update.message.reply_text(f"✅ Broadcast sent to {sent} users.")


# ── Channel post forwarder ─────────────────────────────────────────
async def channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post
    if not post:
        return
    users = load_users()
    sent = 0
    for user_id in users:
        try:
            await context.bot.copy_message(
                chat_id=int(user_id),
                from_chat_id=post.chat.id,
                message_id=post.message_id,
                reply_markup=poster2_markup
            )
            sent += 1
        except Exception as e:
            print(e)
    print(f"Channel post forwarded to {sent} users")


# ── App setup ─────────────────────────────────────────────────────
app = Application.builder().token(BOT_TOKEN).build()
scheduler.start()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.ChatType.CHANNEL, channel_post))

print("✅ Bot is running...")
app.run_polling()
