import asyncio
from celery import Celery
from aiogram import Bot
from config import REDIS_URL, API_TOKEN


API_TOKEN = API_TOKEN  # Замените на ваш токен
bot = Bot(token=API_TOKEN)


celery_app = Celery(
    'tasks',
    broker=f'redis://{REDIS_URL}/0',
    backend=f'redis://{REDIS_URL}/0',
)

async def send_message(chat_id, message):
    await bot.send_message(chat_id, message)

def run_async(func, *args):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(func(*args))

@celery_app.task
def send_message_task(chat_id, message):
    run_async(send_message, chat_id, message)
