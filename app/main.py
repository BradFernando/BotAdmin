import logging
import sys
import json
import os
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from g4f.client import Client
import asyncio

# Import the function from keyboard.py
from tools.keyboard import create_keyboard_markup, create_bot_options_markup, create_more_options_markup

# Import the handlers from handlers.py
from utils.handlers import command_start_handler, echo_handler, callback_query_handler

# Configure the event loop policy for Windows
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Initialize g4f client
client = Client()

# Load environment variables
load_dotenv()
TOKEN = getenv("BOT_TOKEN")

# Initialize dispatcher
dp = Dispatcher()

# Inicializar InlineKeyboardMarkup con inline_keyboard vacío
screen_button = InlineKeyboardMarkup(inline_keyboard=[])

# Use the function to create keyboard_markup
keyboard_markup = create_keyboard_markup()

# Get the base directory
base_dir = os.path.dirname(os.path.abspath(__file__))


async def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error al cargar {file_path}: {e}")
        return {}


@dp.message(CommandStart())
async def start_message(message: Message):
    await command_start_handler(message, keyboard_markup)


@dp.message()
async def echo_message(message: Message):
    await echo_handler(message, load_json, base_dir, client)


@dp.callback_query()
async def handle_callback_query(callback_query: CallbackQuery):
    await callback_query_handler(callback_query, dp)


async def main() -> None:
    # Initialize Bot instance with default properties
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
