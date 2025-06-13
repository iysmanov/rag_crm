import os
import tempfile
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile
from aiogram.utils.markdown import hbold
from config import Config
from rag_engine import KnowledgeBaseRAG
from ocr_engine import extract_text_from_image
from gpt_engine import generate_answer
from logger import log_message
from crm_database import CRMDatabase

import asyncio

# Инициализация бота и движков
bot = Bot(token=Config.TELEGRAM_BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher()
rag = KnowledgeBaseRAG(Config.KNOWLEDGE_BASE_PATH)
crm_db = CRMDatabase()

async def split_and_send(message: types.Message, text: str):
    """Делит длинный ответ на части и отправляет их по очереди."""
    max_len = Config.MAX_ANSWER_LENGTH
    for i in range(0, len(text), max_len):
        await message.answer(text[i:i+max_len])

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот-помощник фитнес-студии WAY2fit.\n\n"
        "Я могу:\n"
        "📅 Показать расписание занятий\n"
        "📋 Рассказать о правилах студии\n"
        "👤 Проверить ваш абонемент\n"
        "❓ Ответить на другие вопросы\n\n"
        "Просто напишите ваш вопрос или используйте команды:\n"
        "/schedule - расписание на сегодня\n"
        "/rules - правила студии\n"
        "/check - проверить абонемент"
    )

@dp.message(Command("schedule"))
async def cmd_schedule(message: types.Message):
    """Показывает расписание на сегодня."""
    schedule = crm_db.get_schedule()
    if schedule.empty:
        await message.answer("На сегодня занятий нет 😔")
        return

    response = "📅 Расписание на сегодня:\n\n"
    for _, row in schedule.iterrows():
        response += (
            f"🕒 {row['StartTime'].strftime(Config.TIME_FORMAT)} - "
            f"{row['EndTime'].strftime(Config.TIME_FORMAT)}\n"
            f"🏋️ {row['ClassName']}\n"
            f"👤 Тренер: {row['TrainerName']}\n"
            f"📍 Зал: {row['RoomName']}\n"
            f"👥 Мест: {row['CurrentBookings']}/{row['MaxCapacity']}\n\n"
        )
    
    await split_and_send(message, response)

@dp.message(Command("rules"))
async def cmd_rules(message: types.Message):
    """Показывает правила студии."""
    rules = crm_db.get_studio_rules()
    if rules.empty:
        await message.answer("Правила временно недоступны 😔")
        return

    response = "📋 Правила студии:\n\n"
    current_category = None
    for _, row in rules.iterrows():
        if current_category != row['RuleCategory']:
            current_category = row['RuleCategory']
            response += f"\n🔹 {current_category}:\n"
        response += f"• {row['RuleDescription']}\n"
    
    await split_and_send(message, response)

@dp.message(Command("check"))
async def cmd_check(message: types.Message):
    """Проверяет информацию об абонементе."""
    await message.answer(
        "Пожалуйста, отправьте номер телефона, указанный при регистрации.\n"
        "Формат: +7XXXXXXXXXX"
    )

@dp.message(F.text.regexp(r'^\+7\d{10}$'))
async def check_membership(message: types.Message):
    """Обрабатывает запрос на проверку абонемента."""
    phone = message.text
    client_info = crm_db.get_client_info(phone)
    
    if client_info.empty:
        await message.answer("❌ Клиент не найден. Проверьте номер телефона.")
        return
    
    client = client_info.iloc[0]
    response = (
        f"👤 Информация о клиенте:\n\n"
        f"Имя: {client['FirstName']} {client['LastName']}\n"
        f"Тип абонемента: {client['MembershipType']}\n"
        f"Действует до: {client['ExpiryDate'].strftime(Config.DATE_FORMAT)}\n"
        f"Осталось занятий: {client['RemainingClasses']}"
    )
    
    await message.answer(response)

@dp.message()
async def handle_message(message: types.Message):
    """Обрабатывает все остальные сообщения."""
    user_id = message.from_user.id
    user_text = message.text or ""
    ocr_text = ""

    # Если есть фото — сохраняем и делаем OCR
    if message.photo:
        photo = message.photo[-1]
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            await photo.download(destination=tmp.name)
            ocr_text = extract_text_from_image(tmp.name)
            os.unlink(tmp.name)
    elif message.document and message.document.mime_type.startswith('image/'):
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            await message.document.download(destination=tmp.name)
            ocr_text = extract_text_from_image(tmp.name)
            os.unlink(tmp.name)

    # Объединяем текст из OCR и текст сообщения
    full_query = '\n'.join([user_text, ocr_text]).strip()
    if not full_query:
        await message.answer("Пожалуйста, отправьте текст или изображение с текстом.")
        return

    # Поиск по базе знаний
    kb_chunks = rag.search(full_query, top_k=Config.MAX_CONTEXT_CHUNKS)
    # Генерация ответа
    answer = generate_answer(full_query, kb_chunks)
    # Логирование
    log_message(user_id, full_query, answer)
    # Отправка ответа
    await split_and_send(message, answer)

if __name__ == "__main__":
    try:
        asyncio.run(dp.start_polling(bot))
    finally:
        crm_db.close() 