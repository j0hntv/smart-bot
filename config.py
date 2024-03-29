import logging
import os
import telegram


class Handler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def setup_logger(logger):

    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id_to_send_logs = os.getenv('CHAT_ID_TO_SEND_LOGS')

    bot = telegram.Bot(token=telegram_bot_token)

    handler = Handler(bot, chat_id_to_send_logs)
    formatter = logging.Formatter(f'[{logger.name}] - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger