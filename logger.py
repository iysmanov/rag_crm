import logging
import os
from config import Config

# Создаём директорию для логов, если нет
os.makedirs(os.path.dirname(Config.LOG_PATH), exist_ok=True)

logging.basicConfig(
    filename=Config.LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    encoding='utf-8'
)

def log_message(user_id, user_input, bot_response):
    """
    Логирует запрос пользователя и ответ бота.
    """
    logging.info(f'USER {user_id}: {user_input}\nBOT: {bot_response}\n---') 