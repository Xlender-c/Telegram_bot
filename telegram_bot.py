# telegram_bot.py
import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Handler Functions ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message with three inline buttons."""
    # Define the layout of the inline keyboard buttons
    keyboard = [
        [InlineKeyboardButton("💬 چت با هوش مصنوعی", callback_data="start_chat")],
        [InlineKeyboardButton("🎨 ساخت عکس", callback_data="create_image")],
        [InlineKeyboardButton("🎙️ گفتگوی صوتی", callback_data="voice_convo")],
    ]
    
    # Create the InlineKeyboardMarkup object
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"سلام {user_name}! لطفاً یک گزینه را انتخاب کنید:", 
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery from a button press."""
    query = update.callback_query
    
    # Answer the query to show the user that the button press was received
    await query.answer()
    
    selected_option = query.data
    
    response_text = ""
    if selected_option == "start_chat":
        response_text = "شما حالت 'چت با هوش مصنوعی' را انتخاب کردید. حالا می‌توانید سوال خود را بپرسید."
        # TODO: This will later connect to the main AI logic
        
    elif selected_option == "create_image":
        response_text = "شما 'ساخت عکس' را انتخاب کردید. لطفاً توضیح عکس مورد نظر خود را بنویسید."
        # TODO: This will later connect to the image generation logic
        
    elif selected_option == "voice_convo":
        response_text = "شما 'گفتگوی صوتی' را انتخاب کردید. لطفاً پیام صوتی خود را ارسال کنید."
        # TODO: This will later connect to the voice processing logic
        
    # Edit the original message to show the user's choice
    await query.edit_message_text(text=response_text)


def main() -> None:
    """Run the bot."""
    # Reads the bot token from an environment variable for security
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("No TELEGRAM_BOT_TOKEN set in environment. Please set it on the Render dashboard.")

    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers for the /start command and button clicks
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot
    print("Bot is running with Inline Keyboard... Press Ctrl-C to stop.")
    application.run_polling()


if __name__ == "__main__":
    main()