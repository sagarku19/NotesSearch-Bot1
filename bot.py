import os
import logging
import google.generativeai as genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.error import BadRequest

# =================== CONFIG ===================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CHANNEL_LINK = "https://t.me/notessearchin"
INSTAGRAM_LINK = "https://instagram.com/notessearch.in"
FREE_DRIVE_LINK = "https://drive.google.com/drive/folder/your-folder-id"
WEBSITE_LINK = "https://upsc.notessearch.in"
SUPPORT_EMAIL = "notessearchin@gmail.com"

# Logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# =================== SYSTEM PROMPT ===================
BOT_PROMPT = """
You are an AI-powered Telegram assistant for NotesSearch.in.

Role & Personality:
- Act like a friendly and knowledgeable course counselor.
- Communicate clearly, politely, and in a student-friendly tone.
- Always sound supportive and motivating, like a guide who wants students to succeed.

What you know about NotesSearch.in:
- NotesSearch provides study material for UPSC, JEE, NEET, and GATE.
- Resources include: detailed notes, PYQs (Previous Year Questions), revision mind maps, and mock tests.
- The main link for students: https://upsc.notessearch.in
- Students can access free material and also purchase paid courses.
- For joining or pricing, always guide: "Click the Buy Now button on our website 👉 upsc.notessearch.in"

Rules:
1. Exam-specific questions → Explain resources + always link to upsc.notessearch.in
2. Pricing/joining → "Just click Buy Now button 👉 upsc.notessearch.in"
3. Study tips → Motivational + connect to NotesSearch
4. Irrelevant → Redirect politely back to study resources
5. Greetings → Warm welcome & ask exam focus
"""

# Create Gemini model
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=BOT_PROMPT
)

# =================== START MESSAGE ===================
async def send_welcome_message(chat_id, bot_instance):
    """Sends a formatted welcome message with buttons."""
    keyboard = [
        [InlineKeyboardButton("💬 Chat with Bot", callback_data="chat_with_bot")],
        [InlineKeyboardButton("ℹ️ About NotesSearch", callback_data="about")],
        [InlineKeyboardButton("🆘 Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "👋 *Welcome to NotesSearch Bot* 📚\n\n"
        "✨ Your AI-powered study companion for _UPSC, JEE, NEET & GATE_ ✨\n\n"
        "Here’s what I can help you with:\n"
        "✅ Access Free & Premium Notes\n"
        "✅ Previous Year Questions (PYQs)\n"
        "✅ Revision Mind Maps\n"
        "✅ Mock Tests & Practice Resources\n"
        "✅ Smart Study Guidance\n\n"
        "⚡ _Pro Tip:_ Just type your question or click a button below 👇"
    )

    await bot_instance.send_message(
        chat_id=chat_id,
        text=welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )

# =================== COMMANDS & HANDLERS ===================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    await send_welcome_message(update.effective_chat.id, context.bot)

async def new_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Auto-send start message when a new chat is opened."""
    for member in update.message.new_chat_members:
        if member.is_bot:
            await send_welcome_message(update.effective_chat.id, context.bot)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles all button clicks."""
    query = update.callback_query
    await query.answer()

    try:
        if query.data == "chat_with_bot":
            await query.message.reply_text(
                "👋 Hi there, I’m your *NotesSearch Study Assistant* 🤖\n\n"
                "Ask me _anything_ about:\n"
                "📚 UPSC, JEE, NEET, GATE preparation\n"
                "📝 Notes, PYQs & Mock Tests\n"
                "💡 Study strategies & motivation\n\n"
                "✨ I’m here to guide you towards success. So, tell me — _which exam are you preparing for?_",
                parse_mode="Markdown",
            )
        
        elif query.data == "about":
            keyboard = [
                [InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_LINK)],
                [InlineKeyboardButton("📢 Join Telegram", url=CHANNEL_LINK)],
                [InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_LINK)],
                [InlineKeyboardButton("📂 Free Drive Link", url=FREE_DRIVE_LINK)],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            about_text = (
                "📖 *About NotesSearch*\n\n"
                "NotesSearch is your *one-stop learning partner* 🚀\n\n"
                "✨ *What we offer:*\n"
                "🔹 UPSC, JEE, NEET & GATE study material\n"
                "🔹 Handwritten + Printed Notes (Hindi & English)\n"
                "🔹 Organized Study Plans & Toppers’ Notes\n"
                "🔹 Daily Free PDFs & Updates\n"
                "🔹 Community Support via Telegram\n\n"
                "📍 _Explore now:_ [upsc.notessearch.in](https://upsc.notessearch.in)"
            )

            await query.message.reply_text(
                about_text,
                parse_mode="Markdown",
                reply_markup=reply_markup,
            )

        elif query.data == "help":
            keyboard = [
                [InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_LINK)],
                [InlineKeyboardButton("📢 Telegram", url=CHANNEL_LINK)],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            help_text = (
                "🆘 *Help & Support*\n\n"
                "If you face any issues or have queries:\n\n"
                f"📧 Email: `{SUPPORT_EMAIL}`\n"
                f"🌐 Website: [upsc.notessearch.in](https://upsc.notessearch.in)\n"
                f"📸 Instagram: [notessearch.in](https://instagram.com/notessearch.in)\n\n"
                "💡 Our team is always ready to assist you!"
            )

            await query.message.reply_text(
                help_text,
                parse_mode="Markdown",
                reply_markup=reply_markup,
            )
        else:
            logger.warning(f"Unknown callback data: {query.data}")
            await query.message.reply_text(
                "⚠ I'm not sure what to do with that. Please choose from the buttons provided."
            )
            
    except Exception as e:
        logger.error(f"Error handling button: {e}")
        await query.message.reply_text("⚠ Something went wrong. Please try again.")

# =================== GEMINI AI REPLY ===================
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends user messages to the Gemini AI model and replies with engaging format."""
    user_msg = update.message.text
    try:
        response = model.generate_content(user_msg)
        raw_reply = response.text if response and response.text else (
            "⚠ Sorry, I couldn’t generate a reply. Please try again."
        )

        reply_text = (
            "💡 *Here’s a helpful answer for you:*\n\n"
            f"{raw_reply.replace('. ', '.\n🔹 ')}\n\n"
            "━━━━━━━\n"
            "✨ _Keep learning and stay consistent!_\n"
            f"👉 More resources available at: [upsc.notessearch.in](https://upsc.notessearch.in)"
        )

        try:
            await update.message.reply_text(reply_text, parse_mode="Markdown")
        except BadRequest as e:
            logger.warning(f"Markdown failed, sending plain text. Error: {e}")
            await update.message.reply_text(raw_reply)

    except Exception as e:
        logger.error(f"AI reply error: {e}")
        error_message = (
            "⚠ Sorry, there was an issue processing your request.\n\n"
            "💡 Please try again, or check out study material here:\n"
            f"[upsc.notessearch.in](https://upsc.notessearch.in)"
        )
        await update.message.reply_text(error_message, parse_mode="Markdown")

# =================== MAIN ===================
def main():
    """Initializes and runs the bot."""
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        logger.error("Error: TELEGRAM_TOKEN or GEMINI_API_KEY environment variables are not set.")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Auto start when chat is opened
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_chat))

    # Start command
    app.add_handler(CommandHandler("start", start))

    # Buttons
    app.add_handler(CallbackQueryHandler(button_handler))

    # AI reply
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    # Error handler
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
        logger.error(msg="Exception while handling an update:", exc_info=context.error)
        if isinstance(update, Update) and update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    "⚠ Oops! Something went wrong.\n"
                    "💡 Please try again later or visit: [upsc.notessearch.in](https://upsc.notessearch.in)"
                ),
                parse_mode="Markdown",
            )

    app.add_error_handler(error_handler)

    print("🤖 NotesSearch Bot with Gemini AI is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
