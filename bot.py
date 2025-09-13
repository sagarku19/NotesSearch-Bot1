import os
import asyncio
import google.generativeai as genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# =================== CONFIG ===================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CHANNEL_USERNAME = "notessearchin"
CHANNEL_LINK = "https://t.me/notessearchin"
INSTAGRAM_LINK = "https://instagram.com/notessearch.in"
FREE_DRIVE_LINK = "https://drive.google.com/drive/folder/your-folder-id"
WEBSITE_LINK = "https://notessearch.in"
SUPPORT_EMAIL = "notessearchin@gmail.com"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# =================== SYSTEM PROMPT ===================
BOT_PROMPT = """
You are an AI-powered Telegram assistant for NotesSearch.in.

Role & Personality:
- Act like a friendly and knowledgeable course counselor.
- Communicate clearly, politely, and in a student-friendly tone.
- Keep answers short and easy to understand, unless the user asks for detailed explanation.
- Always sound supportive and motivating, like a guide who wants students to succeed.

What you know about NotesSearch.in:
- NotesSearch provides study material for UPSC, JEE, NEET, and GATE.
- Resources include: detailed notes, PYQs (Previous Year Questions), revision mind maps, and mock tests.
- The main website is https://notessearch.in
- Students can access free material and also purchase paid courses.
- For joining or pricing, always guide: "Click the Buy Now button on our website."

How to handle questions:
1. If the question is about UPSC, JEE, NEET, or GATE:
    - Explain what NotesSearch offers for that exam.
    - Mention notes, PYQs, revision mind maps, and mock tests.
    - Encourage the student to visit https://notessearch.in for full details.

2. If the student asks about pricing/joining:
    - Always answer: "You can join easily! Just click the Buy Now button on our website 👉 https://notessearch.in"

3. If the student asks a general study question (like preparation tips):
    - Give helpful, motivational advice.
    - Then connect it back to NotesSearch resources.

4. If the student asks about something unrelated (like jokes, sports, news):
    - Politely say: "I’m here to help with study material and exam preparation."
    - Redirect them back to courses and study help.

5. If the student just greets (Hi/Hello/Good morning):
    - Reply warmly and offer help. Example: "👋 Hello! I’m your NotesSearch study assistant. Which exam are you preparing for?"

6. Always include the website link when talking about NotesSearch resources.

Examples of replies:
- "📚 For UPSC, we provide detailed notes, PYQs, revision mind maps, and mock tests. Visit 👉 https://notessearch.in"
- "For pricing and joining, just click the Buy Now button on our website 👉 https://notessearch.in"
- "We support students preparing for UPSC, JEE, NEET, and GATE. Which exam are you focusing on?"
- "That’s a great question! Consistent practice is key to success. At NotesSearch, we provide PYQs and mock tests to help you practice better."

Always stay consistent with these rules.
"""

# Create Gemini model with system prompt
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=BOT_PROMPT
)

# =================== COMMANDS & HANDLERS ===================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    keyboard = [
        [InlineKeyboardButton("💬 Chat with Bot", callback_data="chat_with_bot")],
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

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles all button clicks."""
    query = update.callback_query
    await query.answer()

    if query.data == "chat_with_bot":
        await query.message.reply_text(
            "Hello there! I'm an AI assistant for NotesSearch.in. "
            "Feel free to ask me anything about study materials, exam preparation, "
            "and our courses. How can I help you today?"
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
        keyboard = [[InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "🆘 *Help & Support*\n\n"
            f"📧 Email: {SUPPORT_EMAIL}\n"
            f"📸 Instagram: {INSTAGRAM_LINK}\n\n"
            "Reach out anytime for queries or support! 💬",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

# =================== GEMINI AI REPLY ===================
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends user messages to the Gemini AI model and replies with the generated response."""
    user_msg = update.message.text
    try:
        response = model.generate_content(user_msg)
        reply = response.text if response and response.text else "Sorry, I couldn’t generate a reply. Please try again."
    except Exception as e:
        reply = f"⚠ Error: {str(e)}"
    await update.message.reply_text(reply)

# =================== MAIN ===================
def main():
    """Initializes and runs the bot."""
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("Error: TELEGRAM_TOKEN or GEMINI_API_KEY environment variables are not set.")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Handlers for the old bot's functionality
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Handler for the new Gemini AI functionality
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    print("🤖 NotesSearch Bot with Gemini AI is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
