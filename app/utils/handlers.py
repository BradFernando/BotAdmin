from aiogram import types, html
from fuzzywuzzy import process
import logging
import os

from app.tools.keyboard import create_bot_options_markup, create_more_options_markup, create_keyboard_markup

# Una lista para almacenar el historial de la conversación
conversation_history = []


def is_question_in_context(question: str) -> bool:
    context_keywords = ["administración", "establecimiento", "bot", "restaurante", "platos", "pedidos", "comida"]
    for keyword in context_keywords:
        if keyword in question.lower():
            return True
    return False


def handle_error(e, user_message):
    if isinstance(e, ConnectionError):
        return (f"Lo siento, {user_message.from_user.full_name}. Parece que estoy teniendo problemas de conexión. Por "
                f"favor, inténtalo de nuevo más tarde.")
    elif isinstance(e, TimeoutError):
        return (f"Lo siento, {user_message.from_user.full_name}. Mi respuesta está tardando más de lo esperado. Por "
                f"favor, inténtalo de nuevo más tarde.")
    else:
        logging.error(f"Error in GPT response: {e}")
        return "Hubo un error al procesar tu solicitud. 😓 Por favor intenta nuevamente."


async def command_start_handler(message: types.Message, keyboard_markup) -> None:
    # Resetea el historial de la conversación cuando se inicia una nueva sesión
    global conversation_history
    conversation_history = []

    await message.answer(
        f"Hola, {html.bold(message.from_user.full_name)}! 😊 Si eres el administrador de este "
        f"establecimiento te doy la bienvenida. 🎉 No olvides que tu id de usuario es: {message.from_user.id}",
        reply_markup=keyboard_markup
    )


async def echo_handler(message: types.Message, load_json, base_dir, client) -> None:
    global conversation_history

    # Cargar las respuestas predefinidas
    respuestas = await load_json(os.path.join(base_dir, 'rules', 'respuestas.json'))

    # Buscar la mejor coincidencia en las respuestas predefinidas
    best_match, score = process.extractOne(message.text.lower(), respuestas.keys())

    if score >= 90:
        response_dict = respuestas.get(best_match, {'respuesta': 'No se encontró una respuesta adecuada. 😞'})
    else:
        user_message = f"{message.from_user.full_name} dice: {message.text}"
        conversation_history.append({"role": "user", "content": user_message})

        gpt_reglas = await load_json(os.path.join(base_dir, 'rules', 'gpt_reglas.json'))

        # Incluir el historial de la conversación en el mensaje al modelo GPT
        messages = gpt_reglas + conversation_history

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            response_content = response.choices[0].message.content
            response_dict = {'respuesta': response_content}

            # Verificar si la pregunta está en contexto
            if not is_question_in_context(message.text):
                response_dict = {'respuesta': 'Este bot solo puede responder preguntas sobre la administración del '
                                              'establecimiento y los pedidos de comida. Por favor, formula una '
                                              'pregunta relacionada.'}
            else:
                # Añadir la respuesta del bot al historial de la conversación
                conversation_history.append({"role": "assistant", "content": response_content})
        except Exception as e:
            response_dict = {'respuesta': handle_error(e, message)}

    await message.answer(response_dict['respuesta'])


async def callback_query_handler(callback_query: types.CallbackQuery, dp) -> None:
    data = callback_query.data

    if data == "program_desc":
        await callback_query.message.answer(
            "Descripción del programa: Este bot fue diseñado para ayudarte a manejar tu establecimiento. 🏢")
    elif data == "ask_bot":
        bot_options_markup = create_bot_options_markup()
        await callback_query.message.answer("Elige una opción: 📝", reply_markup=bot_options_markup)
    elif data == "more_options":
        more_options_markup = create_more_options_markup()
        await callback_query.message.answer("Más opciones: 📚", reply_markup=more_options_markup)
    elif data == "order_food":
        await callback_query.message.answer(
            "Para realizar un pedido deberás dirigirte a la parte inferior izquierda de tu teclado donde estaremos "
            "gustosos de que manejes nuestro programa 🍽️")
    elif data == "bot_developers":
        await callback_query.message.answer(
            "Fui desarrollado por dos Estudiantes de la carrera de ITIN Espe Bradley Corro y Jhostyn Gavilanes 👨‍💻‍💻")
    elif data == "end_request":
        await callback_query.message.answer("Ok! Estoy feliz de haberte ayudado. ¡Gracias! 😊")
    elif data == "exit_conversation":
        await callback_query.message.answer("Has salido de la conversación. Usa /start para comenzar de nuevo. 👋")
    elif data == "ask_about_orders":
        await callback_query.message.answer(
            "El usuario que maneje este bot debe de tener en cuenta que los pedidos y pagos únicamente se harán a "
            "través de la aplicación. 💳")
    elif data == "restart_conversation":
        await callback_query.message.answer("Reiniciando conversación... 🔄")
        await command_start_handler(callback_query.message, create_keyboard_markup())

    await callback_query.answer()  # Acknowledge the callback query
