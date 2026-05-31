from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = "8264438185:AAEGGRgQ5_FU-ERfoEZU05IPtywuLorU8ss"
CHANNEL_LINK = "https://t.me/+R9YjIH3JprU5MGU1"

keyboard = [
    [InlineKeyboardButton("🥳 FREE VIP GROUP", url="https://t.me/+R9YjIH3JprU5MGU1")],
    [InlineKeyboardButton("📊 CONTACT OWNER", url="https://t.me/GautamTraderAdmin?text=Hello%20Gautam%20Sir%2C%20I%20am%20interested%20in%20earning%20money%20%F0%9F%92%B0")]
]
reply_markup = InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    with open("users.txt", "a+") as f:
        f.seek(0)
        users = f.read().splitlines()
        if user_id not in users:
            f.write(user_id + "\n")
    await update.message.reply_text(
        f"🚀 Welcome to Gautam GT VIP!\n\nJoin Channel:\n{CHANNEL_LINK}",
        reply_markup=reply_markup
    )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = " ".join(context.args)
    with open("users.txt", "r") as f:
        users = f.read().splitlines()
    sent = 0
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message)
            sent += 1
        except:
            pass
    await update.message.reply_text(f"Broadcast sent to {sent} users.")

async def channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post
    if not post:
        return
    with open("users.txt", "r") as f:
        users = f.read().splitlines()
    sent = 0
    for user_id in users:
        try:
            await context.bot.copy_message(
    chat_id=int(user_id),
    from_chat_id=post.chat.id,
    message_id=post.message_id,
    reply_markup=reply_markup
)
            sent += 1
        except Exception as e:
            print(e)
    print(f"Forwarded to {sent} users")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.ALL, channel_post))
print("Bot is running...")
app.run_polling()