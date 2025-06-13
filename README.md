# Fitness Admin Bot (RAG + GPT-4 + CRM)

Телеграм-бот для фитнес-студии WAY2fit с поддержкой Retrieval-Augmented Generation (RAG), GPT-4 и интеграцией с CRM-системой.

## Возможности
- 📅 Показ расписания занятий
- 📋 Информация о правилах студии
- 👤 Проверка абонементов клиентов
- 💬 Ответы на общие вопросы
- 📸 Распознавание текста с изображений (OCR)
- 🔍 Поиск информации в базе знаний
- 📝 Генерация ответов с помощью GPT-4
- 📊 Интеграция с CRM-системой (MS SQL Server)

## Быстрый старт

1. **Клонируйте репозиторий или скачайте код**

2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Создайте файл настроек `.env`:**
   ```
   # OpenAI и Telegram
   OPENAI_API_KEY=sk-...
   TELEGRAM_BOT_TOKEN=123456:ABC...

   # CRM Database
   CRM_SERVER=localhost
   CRM_DATABASE=fitness_crm
   CRM_USERNAME=sa
   CRM_PASSWORD=your_password

   # Пути
   KNOWLEDGE_BASE_PATH=knowledge_base
   LOG_PATH=log/bot.log
   ```

4. **Подготовьте базу данных CRM:**
   - Создайте базу данных в MS SQL Server
   - Выполните SQL-скрипты для создания таблиц (см. `database/schema.sql`)
   - Заполните таблицы начальными данными

5. **Подготовьте базу знаний:**
   - Создайте папку `knowledge_base/`
   - Добавьте markdown-файлы с информацией о студии

6. **Запустите бота:**
   ```bash
   python main.py
   ```

## Команды бота
- `/start` - приветствие и список возможностей
- `/schedule` - расписание на сегодня
- `/rules` - правила студии
- `/check` - проверить абонемент

## Структура проекта
```
fitness_admin_bot/
├── main.py                # Основной файл Telegram-бота
├── config.py              # Конфигурация
├── crm_database.py        # Работа с CRM (MS SQL)
├── rag_engine.py          # Поиск по базе знаний
├── ocr_engine.py          # Распознавание текста
├── gpt_engine.py          # Генерация ответов (GPT-4)
├── logger.py              # Логирование
├── requirements.txt       # Зависимости
├── Dockerfile            # Для Docker
├── .env                  # Настройки (не в репозитории)
├── knowledge_base/       # База знаний (markdown)
└── log/                  # Логи работы
```

## Структура базы данных
- `Classes` - расписание занятий
- `Trainers` - информация о тренерах
- `Rooms` - информация о залах
- `Clients` - информация о клиентах
- `Memberships` - информация об абонементах
- `StudioRules` - правила студии
- `ClassBookings` - записи на занятия

## Docker
Для запуска в Docker:
```bash
docker build -t fitness-bot .
docker run -d --env-file .env fitness-bot
```

## Требования
- Python 3.8+
- MS SQL Server
- OpenAI API ключ
- Telegram Bot Token

## Поддержка
По вопросам работы бота обращайтесь: t.me/your_support
