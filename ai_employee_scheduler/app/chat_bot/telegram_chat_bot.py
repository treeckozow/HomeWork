# app/bot.py
import os
# import asyncio #, nest_asyncio
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from app.schedule import ai_processing

# nest_asyncio.apply()

# Set your API_URL if different (e.g., if hosted externally)
API_URL = os.getenv("API_URL") # "http://localhost:8000"

# IMPORTANT: Set your Telegram Bot Token in the environment variable TELEGRAM_BOT_TOKEN
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") # "7938912665:AAEJN1FEyWxGQP_Vt9aWb4Rdrt64Fa57Qk4" # <-- Replace or set env var

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Scheduling Bot! Please submit your constraints.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    constraint_text = update.message.text
    # Map Telegram user ID to your system user ID if needed
    payload = {"user_id": user_id, "constraint_text": constraint_text}
    user = ai_processing.createNewUser(constraint_text)
    await update.message.reply_text(user)
    # try:
    #     response = requests.post(f"{API_URL}/submit_constraint", json=payload)
    #     if response.status_code == 200:
    #         await update.message.reply_text("Your constraint has been submitted.")
    #     else:
    #         await update.message.reply_text(f"Error submitting constraint. {response}, {response.status_code}")
    # except Exception as e:
    #     await update.message.reply_text(f"Error connecting to scheduling service. {e}")

def start_bot():
    # Build the Telegram application using your bot token
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Add the command handler for /start
    application.add_handler(CommandHandler("start", start))
    # Add a message handler that handles non-command text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until manually stopped
    application.run_polling()

# Run the async main function.
if __name__ == '__main__':
    start_bot()
