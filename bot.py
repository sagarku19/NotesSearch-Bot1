from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import os

# Load Bot Token from Railway environment
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Your Google Drive link
DRIVE_LINK = "https://drive.google.com/drive/folder/your-folder-id"

# Handle new members joining a group
async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.new_chat_members:
        for member in update.message.new_chat_members:
            await update.message.reply_text(
                f"Welcome {member.first_name} 🎉\nHere’s your link: {DRIVE_LINK}"
            )

# Handle /start command (in DM or group)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name} 👋\nHere’s your Drive link: {DRIVE_LINK}"
    )

def main():
    # Create bot application
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_message))
    app.add_handler(CommandHandler("start", start_command))

    # Run bot
    print("🤖 Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
