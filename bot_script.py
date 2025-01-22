from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Replace these with your actual values
BOT_TOKEN = os.environ.get('BOT_TOKEN')  # Get the bot token from environment variables
YOUR_USER_ID = int(os.environ.get('YOUR_USER_ID'))  # Get your user ID from environment variables

# Custom buttons with links
CUSTOM_KEYBOARD = [
    [InlineKeyboardButton("Start Scalping", url="https://cutt.ly/6e31MvII")],
    [InlineKeyboardButton("Getting Started Guide", url="https://cutt.ly/le3104vx")],
    [InlineKeyboardButton("Scalp Tutorials/Community", url="https://t.me/CopyTradersHub/6470")]
]

# Welcome message
WELCOME_MESSAGE = "Welcome to the bot! Use the buttons below to get started."

# Command handler for /start
async def start(update: Update, context: CallbackContext):
    # Store the user's ID when they start the bot
    user_id = update.message.from_user.id
    if "users" not in context.bot_data:
        context.bot_data["users"] = set()
    context.bot_data["users"].add(user_id)

    # Send the welcome message with custom buttons
    reply_markup = InlineKeyboardMarkup(CUSTOM_KEYBOARD)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)

# Handler for broadcast messages
async def broadcast(update: Update, context: CallbackContext):
    # Check if the message is from the admin (you)
    if update.message.from_user.id == YOUR_USER_ID:
        # Get the message text
        message_text = update.message.text

        # Attach the custom keyboard
        reply_markup = InlineKeyboardMarkup(CUSTOM_KEYBOARD)

        # Send the message to all users
        for user_id in context.bot_data.get("users", []):
            try:
                await context.bot.send_message(chat_id=user_id, text=message_text, reply_markup=reply_markup)
            except Exception as e:
                print(f"Failed to send message to {user_id}: {e}")

# Main function to run the bot
def main():
    # Create the bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))  # Handle /start command
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast))  # Handle broadcast messages

    # Start the bot using polling
    application.run_polling()

# Run the bot
if __name__ == "__main__":
    main()