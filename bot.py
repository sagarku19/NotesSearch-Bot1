from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
import os

# ----------------- Config -----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "notessearchin"
CHANNEL_LINK = "https://t.me/notessearchin"
INSTAGRAM_LINK = "https://instagram.com/notessearch.in"
FREE_DRIVE_LINK = "https://drive.google.com/drive/folders/1BpeKDhMBEIYEf5uowtSAxvCDkMOba3ZG?usp=sharing"
WEBSITE_LINK = "https://notessearch.in"
SUPPORT_EMAIL = "notessearchin@gmail.com"

# ----------------- Start -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Start", callback_data="start_process")],
        [InlineKeyboardButton("ℹ️ About NotesSearch", callback_data="about")],
        [InlineKeyboardButton("🆘 Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome to *NotesSearch Bot* 📚\n\n"
        "Choose an option below to get started 👇",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ----------------- Button Handler -----------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "start_process":
        keyboard = [[InlineKeyboardButton("📢 Follow Telegram Channel", callback_data="check_channel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "🚀 Great! Let's get started.\n\n"
            "First, please follow our Telegram channel to unlock free notes ⬇️",
            reply_markup=reply_markup
        )

    elif query.data == "about":
        keyboard = [
            [InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_LINK)],
            [InlineKeyboardButton("📢 Join Telegram", url=CHANNEL_LINK)],
            [InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "📖 *About NotesSearch*\n\n"
            "NotesSearch is your one-stop platform for:\n"
            "✨ UPSC, SSC, NEET, JEE Notes & PDFs\n"
            "✨ Handwritten + Printed Notes\n"
            "✨ Organized Study Plans & Toppers’ Notes\n"
            "✨ Daily Updates & Community Support\n\n"
            "We make exam prep easier, smarter & faster 🚀",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "help":
        keyboard = [
            [InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "🆘 *Help & Support*\n\n"
            f"📧 Email: {SUPPORT_EMAIL}\n"
            f"📸 Instagram: {INSTAGRAM_LINK}\n\n"
            "Reach out anytime for queries or support! 💬",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "check_channel":
        user_id = query.from_user.id
        try:
            member = await context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
            if member.status in ["member", "administrator", "creator"]:
                # Send drive link
                await query.message.reply_text(
                    f"✅ Thanks for joining our channel!\n\nHere’s your free Drive link 📂:\n{FREE_DRIVE_LINK}"
                )

                # Send Instagram follow message
                keyboard = [[InlineKeyboardButton("📸 Follow on Instagram", url=INSTAGRAM_LINK)]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await query.message.reply_text(
                    "✨ To unlock *more important books*:\n"
                    "➡️ Follow us on Instagram & send the message *'Drive'* there.\n",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )

                # Schedule UPSC Package message after 2 minutes
                await asyncio.sleep(120)
                await send_upsc_package(query.message.chat_id, context)

            else:
                await query.message.reply_text(
                    "❌ You haven’t joined the channel yet. Please join here and try again:\n"
                    f"{CHANNEL_LINK}"
                )
        except Exception:
            await query.message.reply_text(
                "⚠️ Please make sure you joined the channel first:\n"
                f"{CHANNEL_LINK}"
            )

# ----------------- UPSC Package -----------------
async def send_upsc_package(chat_id, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📦 *What You’ll Get in This UPSC Package*\n\n"
        "✅ Full UPSC Syllabus + 9-Month Topper Roadmap\n"
        "✅ Handwritten & Printed Notes (Hindi + English)\n"
        "✅ GS Papers 1–4 Notes & Books (Hindi + English)\n"
        "✅ CSAT Notes & Books (Hindi + English)\n"
        "✅ NCERT (6–12) Notes & Books (Hindi + English)\n"
        "✅ 200+ Standard Books & 2000+ Organized PDFs\n"
        "✅ Toppers’ Notes, Answer Sheets & Study Plans\n"
        "✅ Previous Year Prelims + Mains Qs with Solutions\n"
        "✅ Budget, Economic Survey & Current Affairs (Monthly Updates)\n"
        "✅ Maps, Spectrum Notes, Coaching Materials (5+ Institutes)\n"
        "✅ Test Series, Mock Tests & Practice Sets\n"
        "✅ Telegram Community Support & Monthly Updated Material\n\n"
        "🎯 *One-Stop Solution for UPSC Prep – Save Time, Study Smart!*\n\n"
        "🌐 See samples on our official website\n"
        "📩 For any query, connect with our team"
    )

    keyboard = [
        [InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_LINK)],
        [InlineKeyboardButton("📢 Join Telegram", url=CHANNEL_LINK)],
        [InlineKeyboardButton("📸 Follow Instagram", url=INSTAGRAM_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=reply_markup)

# ----------------- Main -----------------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
