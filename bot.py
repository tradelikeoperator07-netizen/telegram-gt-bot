import json, os, asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

BOT_TOKEN = "8264438185:AAEGGRgQ5_FU-ERfoEZU05IPtywuLorU8ss"
USERS_FILE = "users.json"

# ── TEST MODE: all delays = 1 minute ─────────────────────────────
# Change to False when ready for production
TEST_MODE = True

def mins(m):
    return timedelta(minutes=1) if TEST_MODE else timedelta(minutes=m)

def hours(h):
    return timedelta(minutes=1) if TEST_MODE else timedelta(hours=h)


# ── Inline Keyboards ──────────────────────────────────────────────
msg1_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔴 JOIN FREE GROUP CLICK 📈", url="https://telegram.me/+4Ds1pUXu4VUzMzhl")],
    [InlineKeyboardButton("🟢 CONTACT OWNER 🤝", url="https://t.me/Alphaz_Admin?text=Alpha%20Sir%2C%20I%20Want%20To%20Build%20A%20Lifestyle%20Like%20Yours.%20Please%20Guide%20Me%20On%20The%20Process%20To%20Join%20Your%20VIP%E2%9D%A4%EF%B8%8F%F0%9F%94%A5")]
])

# Message 2 - ALPHA2cirvideo (instant) - now has 2 buttons
msg2_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔴 JOIN FREE GROUP CLICK 📈", url="https://telegram.me/+4Ds1pUXu4VUzMzhl")],
    [InlineKeyboardButton("🟢 CONTACT OWNER 🤝", url="https://t.me/Alphaz_Admin?text=Alpha%20Sir%2C%20I%20Want%20To%20Build%20A%20Lifestyle%20Like%20Yours.%20Please%20Guide%20Me%20On%20The%20Process%20To%20Join%20Your%20VIP%E2%9D%A4%EF%B8%8F%F0%9F%94%A5")]
])

# Message 3 - alphavidoe2 circle video (+15 min) - now has 1 button
msg3_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("🤖🔥 GET SIGNAL BOT ACCESS", url="https://t.me/Alphaz_Admin?text=Alpha%20Sir,%20I%20Want%20Your%20Quotex%20Signal%20Bot%20%F0%9F%A4%96%F0%9F%94%A5%0A%0APlease%20Guide%20Me%20On%20The%20Process%20To%20Get%20Access.%20%E2%9D%A4%EF%B8%8F")]
])

msg4_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔴 JOIN FREE GROUP CLICK 📈", url="https://telegram.me/+4Ds1pUXu4VUzMzhl")],
    [InlineKeyboardButton("🟢 CONTACT OWNER 🤝", url="https://t.me/Alphaz_Admin?text=Alpha%20Sir%2C%20I%20Want%20To%20Build%20A%20Lifestyle%20Like%20Yours.%20Please%20Guide%20Me%20On%20The%20Process%20To%20Join%20Your%20VIP%E2%9D%A4%EF%B8%8F%F0%9F%94%A5")]
])

msg5_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔴 JOIN FREE GROUP CLICK 📈", url="https://telegram.me/+4Ds1pUXu4VUzMzhl")],
    [InlineKeyboardButton("📉 LOSS RECOVERY 🙏", url="https://t.me/Alphaz_Admin?text=Alpha%20Sir%2C%20I%20Want%20To%20Recover%20My%20Losses.%0A%0APlease%20Guide%20Me%20And%20Help%20Me%20Join%20Your%20VIP")]
])

msg6_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("🚀 JOIN SESSION ❤️🔥", url="https://t.me/Alphaz_Admin?text=Alpha%20Sir%2C%20I%20Want%20To%20Join%20Your%20Public%20Session%20%F0%9F%9A%80%0A%0APlease%20Guide%20Me%20On%20How%20To%20Participate%20And%20Learn%20From%20You.%20%E2%9D%A4%EF%B8%8F%F0%9F%94%A5")]
])


# ── Captions ──────────────────────────────────────────────────────
MSG1_CAPTION = """<b>💰 You're Here Because You Want To Earn Money! 💰

✅ Join My Channel Below & Start Earning Money 🤩🚀

━━━━━━━━━━━━━━━━━━━━━━
🌟 The Alpha Traderz - Your Path To Profits! 📈
━━━━━━━━━━━━━━━━━━━━━━

👇 Click Below To Join Now!</b>"""

# Message 2 caption (was msg3) - benefits text
MSG2_CAPTION = """<b>🚨 To Continue, Please Join Our Official Channel 🌟

━━━━━━━━━━━━━━━━━━━━━━
⚡️ THE ALPHA TRADERZ ⚡️
━━━━━━━━━━━━━━━━━━━━━━

▶️ 95% Accuracy Trades 📈
▶️ Personal LOSS Recovery 📁
▶️ DAILY BUG TOURNAMENT 📊
▶️ Free 10–15 SIGNALS 🚀
▶️ Full COPY-TRADING Access 🛸
▶️ AI Trading HACKBOT 🤖

━━━━━━━━━━━━━━━━━━━━━━
🔗 JOIN FREE GROUP: https://telegram.me/+4Ds1pUXu4VUzMzhl
━━━━━━━━━━━━━━━━━━━━━━

👇 Choose Your Next Step!</b>"""

MSG4_CAPTION = """<b>💸 You're Here Because You Want To Earn Money! 💰

👀 SEE MY WITHDRAWAL HISTORY 👇
💎 THIS IS HOW A PROFITABLE TRADER LOOKS LIKE! 💎

━━━━━━━━━━━━━━━━━━━━━━
✅ Join My Channel Below & Start Earning Money 🤩
━━━━━━━━━━━━━━━━━━━━━━

👇 Take Action Now!</b>"""

MSG5_CAPTION = """<b>👋 Hello! Are You Ready To Earn Money With Trading? 💰

🚫 No Experience Needed! 🚫

━━━━━━━━━━━━━━━━━━━━━━
🏆 I Helped 10,000+ New Members Start EARNING! 📈
━━━━━━━━━━━━━━━━━━━━━━

📊 These Are The Real Results Of My Clients Earning With Me! 🔥

💪 You Can Be Next! Join Now & Start Your Journey! 🚀

👇 Choose Your Next Step!</b>"""

MSG6_CAPTION = """<b>🚀 Public Trading Session Is LIVE Soon! 🔥

━━━━━━━━━━━━━━━━━━━━━━
⚡️ Don't Miss This Opportunity! ⚡️
━━━━━━━━━━━━━━━━━━━━━━

📈 Learn From The Best & Start Earning Today! 💰

👇 Click Below To Join The Session!</b>"""


# ── Helpers ───────────────────────────────────────────────────────
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

scheduler = AsyncIOScheduler()


# ── Message 6 - ALPHAPUBLIC.PNG (loops every 24 hrs) ─────────────
async def send_msg6_loop(bot, user_id):
    try:
        with open("ALPHAPUBLIC.PNG", "rb") as photo:
            await bot.send_photo(
                chat_id=user_id,
                photo=photo,
                caption=MSG6_CAPTION,
                reply_markup=msg6_markup,
                parse_mode="HTML"
            )
        print(f"✅ Msg6 (Public Session) sent to {user_id}")
    except Exception as e:
        print(f"❌ Msg6 error for {user_id}: {e}")

    scheduler.add_job(
        send_msg6_loop,
        trigger=DateTrigger(run_date=datetime.now() + hours(24)),
        args=[bot, user_id],
        id=f"msg6_loop_{user_id}",
        replace_existing=True
    )
    print(f"🔁 Msg6 loop rescheduled for {user_id}")


# ── Message 5 - 12 Feedback images (+2 hours) ────────────────────
async def send_msg5(bot, user_id):
    try:
        media = []
        for i in range(1, 13):
            with open(f"ALPHAFEEDBACK{i}.JPG", "rb") as f:
                data = f.read()
            if i == 12:
                media.append(InputMediaPhoto(data, caption=MSG5_CAPTION, parse_mode="HTML"))
            else:
                media.append(InputMediaPhoto(data))

        await bot.send_media_group(chat_id=user_id, media=media)
        await bot.send_message(
            chat_id=user_id,
            text="👇 Choose your next step:",
            reply_markup=msg5_markup,
            disable_web_page_preview=True
        )
        print(f"✅ Msg5 (Feedback x12) sent to {user_id}")
    except Exception as e:
        print(f"❌ Msg5 error for {user_id}: {e}")

    scheduler.add_job(
        send_msg6_loop,
        trigger=DateTrigger(run_date=datetime.now() + hours(3)),
        args=[bot, user_id],
        id=f"msg6_{user_id}",
        replace_existing=True
    )
    print(f"📅 Msg6 scheduled for {user_id}")


# ── Message 4 - QUOTEXWITH (+30 min) ─────────────────────────────
async def send_msg4(bot, user_id):
    try:
        with open("QUOTEXWITH.JPG", "rb") as w1, open("QUOTEXWITH1.JPG", "rb") as w2:
            await bot.send_media_group(
                chat_id=user_id,
                media=[
                    InputMediaPhoto(w1),
                    InputMediaPhoto(w2, caption=MSG4_CAPTION, parse_mode="HTML"),
                ]
            )
        await bot.send_message(
            chat_id=user_id,
            text="👇 Choose your next step:",
            reply_markup=msg4_markup,
            disable_web_page_preview=True
        )
        print(f"✅ Msg4 (Quotex Withdrawal) sent to {user_id}")
    except Exception as e:
        print(f"❌ Msg4 error for {user_id}: {e}")

    scheduler.add_job(
        send_msg5,
        trigger=DateTrigger(run_date=datetime.now() + hours(2)),
        args=[bot, user_id],
        id=f"msg5_{user_id}",
        replace_existing=True
    )
    print(f"📅 Msg5 scheduled for {user_id}")


# ── Message 3 - alphavidoe2.MP4 circle video (+15 min) ───────────
async def send_msg3(bot, user_id):
    try:
        with open("alphavidoe2.MP4", "rb") as video:
            await bot.send_video_note(
                chat_id=user_id,
                video_note=video
            )
        await bot.send_message(
            chat_id=user_id,
            text="👇 Choose your next step:",
            reply_markup=msg3_markup
        )
        print(f"✅ Msg3 (circle video) sent to {user_id}")
    except Exception as e:
        print(f"❌ Msg3 error for {user_id}: {e}")

    scheduler.add_job(
        send_msg4,
        trigger=DateTrigger(run_date=datetime.now() + mins(30)),
        args=[bot, user_id],
        id=f"msg4_{user_id}",
        replace_existing=True
    )
    print(f"📅 Msg4 scheduled for {user_id}")


# ── /start handler ────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)

    users = load_users()
    if uid not in users:
        users[uid] = {"joined": str(datetime.now())}
        save_users(users)

    # ── Message 1: THEALPHAVIP.PNG (Instant) ─────────────────────
    try:
        with open("THEALPHAVIP.PNG", "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=MSG1_CAPTION,
                reply_markup=msg1_markup,
                parse_mode="HTML"
            )
        print(f"✅ Msg1 sent to {user.first_name}")
    except Exception as e:
        print(f"❌ Msg1 error: {e}")

    # ── Message 2: ALPHA2cirvideo.MP4 + caption + 2 buttons (Instant) ──
    await asyncio.sleep(3)
    try:
        with open("ALPHA2cirvideo.MP4", "rb") as video:
            await update.message.reply_video(
                video=video,
                caption=MSG2_CAPTION,
                reply_markup=msg2_markup,
                parse_mode="HTML"
            )
        print(f"✅ Msg2 (ALPHA2cirvideo + caption) sent to {user.first_name}")
    except Exception as e:
        print(f"❌ Msg2 error: {e}")

    # ── Schedule Message 3: alphavidoe2 circle video after 15 min ─
    scheduler.add_job(
        send_msg3,
        trigger=DateTrigger(run_date=datetime.now() + mins(15)),
        args=[context.bot, user.id],
        id=f"msg3_{user.id}",
        replace_existing=True
    )
    print(f"📅 Msg3 scheduled for {user.first_name} ({'1 min TEST' if TEST_MODE else '15 min'})")


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


# ── App setup ─────────────────────────────────────────────────────
app = Application.builder().token(BOT_TOKEN).build()
scheduler.start()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))

print("✅ Alpha Trader Bot is running... (TEST MODE ON)" if TEST_MODE else "✅ Alpha Trader Bot is running... (PRODUCTION MODE)")
app.run_polling()
