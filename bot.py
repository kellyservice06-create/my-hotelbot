import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Booking(StatesGroup):
    waiting_name = State()

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Book a Room", callback_data="book")]
    ])
    await message.answer("Welcome to MyOtelBot!\nClick below to book", reply_markup=kb)

@dp.callback_query(lambda c: c.data == "book")
async def book(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Please type your full name:")
    await state.set_state(Booking.waiting_name)

@dp.message(Booking.waiting_name)
async def get_name(message: types.Message, state: FSMContext):
    await message.answer(f"Thanks {message.text}! Your booking request was sent.")
    await bot.send_message(ADMIN_ID, f"New booking!\nFrom: @{message.from_user.username}\nName: {message.text}")
    await state.clear()

async def main():
    logging.info("Bot started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
