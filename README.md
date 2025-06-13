# Fitness Admin Bot (RAG + GPT-4)

Телеграм-бот для администраторов фитнес-студии с поддержкой Retrieval-Augmented Generation (RAG) и GPT-4.

## Возможности
- Приём текстовых вопросов и скриншотов переписок (OCR)
- Поиск релевантных советов в базе знаний (markdown)
- Генерация структурированных ответов с помощью GPT-4
- Логирование всех запросов и ответов
- Русский язык, оформление с эмодзи и чек-листами

## Быстрый старт

1. **Клонируйте репозиторий или скачайте код**
2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Создайте файл настроек `.env` или отредактируйте `config.py`:**
   - Пропишите свой OpenAI API-ключ
   - Укажите Telegram Bot Token
   - Укажите путь к папке с базой знаний (markdown)
4. **Положите ваши markdown-файлы с советами в папку `knowledge_base/`**
5. **Запустите бота:**
   ```bash
   python main.py
   ```

## Переменные окружения (`.env`)
```
OPENAI_API_KEY=sk-...
TELEGRAM_BOT_TOKEN=123456:ABC...
KNOWLEDGE_BASE_PATH=knowledge_base
LOG_PATH=bot.log
```

## Структура проекта
- `main.py` — запуск бота
- `config.py` — настройки
- `knowledge_base/` — база знаний (markdown)
- `log/` — логи

## Docker (опционально)
Для запуска в Docker используйте `Dockerfile` (будет добавлен).



Структура проекта

fitness_admin_bot/
├── main.py                # Основной файл Telegram-бота (aiogram)
├── config.py              # Конфиг с настройками (чтение из .env)
├── rag_engine.py          # Индексация и поиск по базе знаний (markdown, FAISS+TFIDF)
├── ocr_engine.py          # OCR на PaddleOCR для скриншотов
├── gpt_engine.py          # Генерация ответа через OpenAI GPT-4
├── logger.py              # Логирование всех запросов и ответов
├── requirements.txt       # Все зависимости
├── Dockerfile             # Для запуска в Docker (опционально)
├── .gitignore             # Исключения для git
├── README.md              # Инструкция по запуску
├── log/                   # Логи работы бота
└── knowledge_base/        # Ваша база знаний (markdown-файлы)
    └── README.md          # Пример и инструкция