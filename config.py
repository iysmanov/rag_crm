import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

class Config:
    """Конфиг для бота: токены, пути, параметры."""
    # OpenAI и Telegram настройки
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'sk-...')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'your-telegram-token')
    
    # Пути к файлам
    KNOWLEDGE_BASE_PATH = os.getenv('KNOWLEDGE_BASE_PATH', 'knowledge_base')
    LOG_PATH = os.getenv('LOG_PATH', 'log/bot.log')
    
    # Параметры генерации ответов
    MAX_CONTEXT_CHUNKS = int(os.getenv('MAX_CONTEXT_CHUNKS', 5))
    MAX_ANSWER_LENGTH = int(os.getenv('MAX_ANSWER_LENGTH', 3500))
    
    # Настройки CRM базы данных
    CRM_SERVER = os.getenv('CRM_SERVER', 'localhost')
    CRM_DATABASE = os.getenv('CRM_DATABASE', 'fitness_crm')
    CRM_USERNAME = os.getenv('CRM_USERNAME', 'sa')
    CRM_PASSWORD = os.getenv('CRM_PASSWORD', '')
    
    # Настройки форматирования расписания
    TIME_FORMAT = '%H:%M'
    DATE_FORMAT = '%d.%m.%Y' 