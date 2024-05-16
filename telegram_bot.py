import os
import json
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update

class TelegramBot:
    def __init__(self, token, dispatcher, data_dir='data'):
        self.token = token
        self.data_dir = data_dir
        self.message_data_file = os.path.join(data_dir, 'message_data.json')
        self.load_message_data()
        self.dispatcher = dispatcher  # Assign the dispatcher object

        # Register handlers
        self.register_handlers()

    def load_message_data(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        if os.path.exists(self.message_data_file):
            with open(self.message_data_file, 'r') as f:
                self.message_data = json.load(f)
        else:
            self.message_data = {}

    def save_message_data(self):
        with open(self.message_data_file, 'w') as f:
            json.dump(self.message_data, f, indent=4)

    def start(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Welcome to the Telegram Analytics Bot!')

    def help(self, update: Update, context: CallbackContext) -> None:
        help_message = """
        Available commands:
        /start - Start the bot
        /help - Show this help message
        /analyze - Perform analysis (placeholder)
        """
        update.message.reply_text(help_message)

    def echo(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        user_id = update.message.from_user.id
        message_text = update.message.text

        # Track the message
        self.track_message(chat_id, user_id, message_text)

        update.message.reply_text(f'You said: {message_text}')

    def track_message(self, chat_id, user_id, message):
        if chat_id not in self.message_data:
            self.message_data[chat_id] = {}
        if user_id not in self.message_data[chat_id]:
            self.message_data[chat_id][user_id] = []

        self.message_data[chat_id][user_id].append({
            'timestamp': str(update.message.date),
            'message': message
        })

        self.save_message_data()

    def analyze(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Analysis completed!')  # Placeholder for analysis logic

    def register_handlers(self):
        # Register command handlers
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("help", self.help))
        self.dispatcher.add_handler(CommandHandler("analyze", self.analyze))  # Register analyze command handler

        # Register message handler
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.echo))

    def run(self):
        # Start the Bot
        updater = Updater(self.token, use_context=True)
        updater.dispatcher = self.dispatcher  # Set the dispatcher
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
        updater.idle()


if __name__ == "__main__":
    # Set your Telegram Bot token here
    token = "TOKEN"

    # Create the Updater and Dispatcher
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # Create the bot instance
    bot = TelegramBot(token, dispatcher)

    # Run the bot
    bot.run()
