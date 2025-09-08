from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os

# Take bot token from Railway Environment
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Your Drive link
DRIVE_LINK = "https://drive.google.com/drive/folder/your-folder-id"

async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.new_chat_members:
        for member in update.message.new_chat_members:
            await update.message.reply_text(
                f"Welcome {member.first_name} 🎉\nHere’s your link: {DRIVE_LINK}"
            )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_message))
    app.run_polling()

if __name__ == "__main__":
    main()
