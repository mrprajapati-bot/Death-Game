import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Define the death number function
async def death_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    death_number = random.randint(1, 9)
    await update.message.reply_text(f"Your death number is: {death_number}")

# Handle text messages
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text.lower() == "death number":
        await death_number(update, context)
    else:
        await update.message.reply_text("Send 'Death number' to receive a death number!")

# Define the start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! Type 'Death number' to get a death no.!!")

# Main function
def main():
    TOKEN = "7996841554:AAGefNt0UsOuqh1gGkUbVBnUYnefQNY6kLc"

    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()

