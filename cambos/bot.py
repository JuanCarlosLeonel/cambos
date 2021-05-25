#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://git.io/JOmFw.
"""

import os
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    Filters
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start():
    return menu()

def menu(update, context):
    from core.models import UserBot

    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    mensagem = update.message.text
    
    try:
        userbot = UserBot.objects.get(user_id = chat_id)
        text = f'Escolha uma opção:'
        dict = {}  
        if userbot.oficina.count() > 0:
            dict['Terceirizados']='terceirizados'

        if userbot.lavanderia:
             dict['Lavanderia']='lavanderia'

        keyboard = []
        for key, value in dict.items():
            keyboard.append(
            [InlineKeyboardButton(key, callback_data = value)]
            )        
        keyboard.append([InlineKeyboardButton('Geral', callback_data = "geral")])  
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(text, reply_markup=reply_markup)

    except:
        p = UserBot(user_id = chat_id, user_nome = first_name)
        p.save() 
        text = f'Olá {first_name}!{os.linesep}Obrigado por acessar nosso sistema.{os.linesep}Já já seu acesso será liberado.'   
        update.message.reply_text(text)    


def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    
    query.answer()
    if query.data == 'lavanderia':
        keyboard = [
        [
            InlineKeyboardButton("Opção 1", callback_data='1'),
            InlineKeyboardButton("Opção 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Opção 3", callback_data='3')],
        ]

        
    if query.data == 'terceirizados':
        keyboard = [
        [
            InlineKeyboardButton("Opção 4", callback_data='4'),
            InlineKeyboardButton("Opção 5", callback_data='5'),
        ],
        [InlineKeyboardButton("Opção 6", callback_data='6')],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text('opção', reply_markup=reply_markup)

    

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("1852462745:AAF02s1SOqvgZlfxlLX8iFb_uzhgrY5T8cM")
    
    
    updater.dispatcher.add_handler(MessageHandler(Filters.text, menu))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    

    updater.start_polling()
    updater.idle()
   

def iniciar():
    from core.models import Bot
    ativo= Bot.objects.latest('token').ativo            
    if ativo:
        return main()



if __name__ == '__main__':
    main()