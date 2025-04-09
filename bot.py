import os
import logging
import psycopg2
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "6848027066:AAGoVJOQ2-hosoAPf6cq5pY5IrrYVXJAIGs"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply("Привет! Я бот, который будет присылать прогнозы на баскетбольные матчи. Чтобы начать отслеживание, используй команду /track")

@dp.message_handler(commands=['track'])
async def track_handler(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("INSERT INTO users (user_id) VALUES (%s) ON CONFLICT DO NOTHING;", (user_id,))
    conn.commit()
    await message.reply("Ты подписан на обновления по выбранным матчам.")

@dp.message_handler(commands=['untrack'])
async def untrack_handler(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("DELETE FROM users WHERE user_id = %s;", (user_id,))
    conn.commit()
    await message.reply("Ты отписан от обновлений.")

@dp.message_handler(commands=['status'])
async def status_handler(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT 1 FROM users WHERE user_id = %s;", (user_id,))
    result = cursor.fetchone()
    if result:
        await message.reply("Ты подписан на обновления.")
    else:
        await message.reply("Ты не подписан. Используй /track для подписки.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
