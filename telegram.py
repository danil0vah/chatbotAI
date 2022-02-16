# -*- coding: utf-8 -*-
import logging

from aiogram import Bot, Dispatcher, executor, types

from chat_bot import chatbot_response

import nest_asyncio



API_TOKEN = 'ENTER_YOUR_TOKEN'

# Конфигурация logging
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    """
    Эта функция вызывается когда вводится команда /start
    """
    await message.reply("Я простой бот с искусственным интеллектом!\nНо сильно не надейся на меня.")


@dp.message_handler()
async def echo(message: types.Message):
    res = chatbot_response(message.text)
    
    # await bot.send_message(message.chat.id, res)

    await message.answer(res)


if __name__ == '__main__':
    nest_asyncio.apply()
    executor.start_polling(dp, skip_updates=True)
    