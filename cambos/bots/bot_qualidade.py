import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)
from qualidade.models import QualidadeBot
from roupa.views import get_url, convert_setor
from dateutil import parser
import datetime


def get_user(update):
    from qualidade.models import QualidadeBot
    user_id = update.message.chat_id
    userbot = QualidadeBot.objects.get(user_id = user_id)
    return userbot

def return_menu(update):
    keyboard = [[InlineKeyboardButton(f'\U000021A9 Menu', callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)    
    update.message.reply_text('\U0001F456', reply_markup=reply_markup)

def qualidade_track(context: CallbackContext):    
    from qualidade.models import QualidadeTrack    
    track_list = QualidadeTrack.objects.latest("pcp")
    user_list = QualidadeBot.objects.filter(ativo = True, pedido_parado = True)    
    for pedido in track_list.pcp:            
        for user in user_list:                        
            chat_id = user.user_id        
            if pedido["tipo"] == "parado":
                if user.pedido_parado:
                    text = f'Novo pedido parado: {pedido["lacre"]}'            
                    
                    keyboard = [
                        [                    
                            InlineKeyboardButton("Relatório", url='https://indicador.souzacambos.com.br/'),
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)            
                    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)            
            if pedido["tipo"] == "acao":
                if chat_id == pedido['responsavel']:                    
                    text = f'Nova Ação sob cadastrada a sua responsabilidade: {pedido["lacre"]}: {pedido["descricao"]}'  
                    keyboard = [
                        [                    
                            InlineKeyboardButton("Relatório", url='https://indicador.souzacambos.com.br/'),
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)            
                    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
                elif user.ver_acoes:                    
                    text = f'Nova Ação cadastrada: {pedido["lacre"]}: {pedido["descricao"]}'                               
                    keyboard = [
                        [                    
                            InlineKeyboardButton("Relatório", url='https://indicador.souzacambos.com.br/'),
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)            
                    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    track_list.pcp = []    
    track_list.save()
        

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start():
    return menu()

def menu(update, context):
    from roupa.models import RoupaBot, User
    chat_id = update.message.chat_id    
    first_name = update.message.chat.first_name    
    try:
        userbot = get_user(update)
        text = f"\U0001F4AC Escolha uma opção:"
        dict = {}  
        if userbot.pedido_parado:
             dict['Parados']='parados'

        keyboard = []
        for key, value in dict.items():
            keyboard.append(
            [InlineKeyboardButton(key, callback_data = value)]
            )                
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

    except:
        p = QualidadeBot(user_id = chat_id, user_nome = first_name)
        p.save() 
        text = f'Olá {first_name}!{os.linesep}Obrigado por acessar nosso sistema.{os.linesep}Já já seu acesso será liberado.'   
        update.message.reply_text(text)    

def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    
    query.answer()
    if query.data == 'parados':
        keyboard = [
        [
            InlineKeyboardButton("Produção em Atraso", callback_data='atraso_geral'),
            InlineKeyboardButton("Produtos Parados", callback_data='parado_geral')
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]
    
    elif query.data == 'menu':
        keyboard = menu(query, 'nav')

    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('\U0001F4AC Escolha uma opção:', reply_markup=reply_markup, parse_mode=ParseMode.HTML)


def main() -> None:
    from core.models import Bot
    bot = Bot.objects.get(nome = 'Qualidade')
    token = bot.token      
    updater = Updater(token)  
    updater.dispatcher.add_handler(MessageHandler(Filters.text, menu))  
    # updater.dispatcher.add_handler(MessageHandler(Filters.text, pesquisa_corte))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    hora = datetime.time(bot.horas, bot.minutos, 00, 000000) # +3 horas
    up_job = updater.job_queue    
    #up_job.run_daily(resumo_diario, time=hora, days=(0, 1, 2, 3, 4, 5)) 
    # up_job.run_daily(entrada_costura, datetime.time(hour=12, minute=35), days=(0, 1, 2, 3, 4, 5))  
    up_job.run_repeating(qualidade_track, interval=60.0, first=0) 
    #up_job.run_once(resumo_diario, 10)
    updater.start_polling()
    updater.idle()

def iniciar():
    from core.models import Bot
    ativo= Bot.objects.get(nome = 'Qualidade').ativo            
    if ativo:
        return main()   

      
if __name__ == '__main__':
    main()