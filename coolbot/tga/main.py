import logging

from aiogram import Bot, Dispatcher, executor, types
from buttons import button
from api import  create_user,create_feedback
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from states import FeedbackState

API_TOKEN = '5935199873:AAGtK7lJ7vltwrJxgchUWB5-Hg3ZgOUWfvo'


logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Assalamu alaykum Aiogram botimzga hush kelibsz", reply_markup=button)
    print(create_user(message.from_user.username, message.from_user.first_name, message.from_user.id))


@dp.message_handler(Text(startswith="Talab va Takliflar"))
async def feedback_1(message: types.Message):
    await message.answer("Xabar matnini kiriting!! ")
    await FeedbackState.body.set()



@dp.message_handler(state=FeedbackState)
async def feedback_2(message: types.Message, state:FSMContext):
    ms=message.text
    print(create_feedback(message.from_user.id, ms))
    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)




