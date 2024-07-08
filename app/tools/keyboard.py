from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_keyboard_markup():
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Descripción del programa 📝", callback_data="program_desc")],
        [InlineKeyboardButton(text="Preguntar al bot 🤖", callback_data="ask_bot")],
        [InlineKeyboardButton(text="Más opciones 📚", callback_data="more_options")]
    ])
    return keyboard_markup


def create_bot_options_markup():
    bot_options_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Quiero realizar un pedido 🍽️", callback_data="order_food")],
        [InlineKeyboardButton(text="Por quien fuiste desarrollado 👨‍💻", callback_data="bot_developers")],
        [InlineKeyboardButton(text="Es todo lo que quiero pedir ✅", callback_data="end_request")]
    ])
    return bot_options_markup


def create_more_options_markup():
    more_options_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Salir 👋", callback_data="exit_conversation")],
        [InlineKeyboardButton(text="¿Preguntar acerca de los pedidos? 💳", callback_data="ask_about_orders")],
        [InlineKeyboardButton(text="Reiniciar Conversación 🔄", callback_data="restart_conversation")]
    ])
    return more_options_markup