from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Bot token from Railway environment
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Links
CHANNEL_LINK = "https://t.me/notessearchin"
INSTAGRAM_LINK = "https://instagram.com/notessearch.in"
FREE_DRIVE_LINK = "https://drive.google.com/drive/folder/your-folder-id"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("📂 Get Free Drive Link", callback_data="get_drive")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Hi {user.first_name} 👋\nWelcome to **NotesSearch Bot** 📚",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Handle button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_drive":
        keyboard = [
            [InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_LINK)],
            [InlineKeyboardButton("📸 Follow on Instagram", url=INSTAGRAM_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = (
            "✨ To access the free Drive link:\n"
            f"👉 First, join our channel: {CHANNEL_LINK}\n\n"
            "📚 About *NotesSearch*:\n"
            "- Daily updated notes & PDFs for UPSC, SSC, NEET, JEE\n"
            "- Free & premium content for all students\n"
            "- Helping students prepare smarter 🚀\n\n"
            f"📸 Follow us on Instagram: {INSTAGRAM_LINK}\n"
            "➡️ Send me 'Drive' on Instagram to unlock **more important book links** 📂"
        )

        await query.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
