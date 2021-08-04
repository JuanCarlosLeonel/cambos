import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    Filters
)
from roupa.views import get_url, convert_setor
from dateutil import parser
import datetime


def get_user(update):
    from core.models import UserBot
    user_id = update.message.chat_id
    userbot = UserBot.objects.get(user_id = user_id)
    return userbot


def get_data(setor, context, oficina=None):
    dados = get_url()    
    contador = 0
    somador = 0    
    for produto in dados:              
        if setor == 12:
            if context == 'atrasado':
                if produto['Atrasado'] == "Atrasado":
                    contador += 1
                    somador += produto['QuantPecas']
            elif context == 'parado':
                if produto['Parado'] == "1":
                    contador += 1
                    somador += produto['QuantPecas']
        elif setor == 5:
            if produto['Status'] == setor:
                if oficina:
                    if produto['Celula'] == oficina:
                        if context == 'atrasado':                        
                            if produto['Atrasado'] == "Em Atraso":            
                                contador += 1
                                somador += produto['QuantPecas']    
                else:
                    if context == 'atrasado':                        
                        if produto['Atrasado'] == "Em Atraso":            
                            contador += 1
                            somador += produto['QuantPecas']    
        else:
            if produto['Status'] == setor:
                if context == 'atrasado':                        
                    if produto['Atrasado'] == "Em Atraso":            
                        contador += 1
                        somador += produto['QuantPecas']    

    return {'contador':contador,'somador':somador}


def return_menu(update, text):
    keyboard = [[InlineKeyboardButton(f'\U000021A9 Menu', callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)    
    update.message.reply_text('\U0001F456', reply_markup=reply_markup)


def producao_em_atraso(update, setor):            
    if setor == 5:
        user = get_user(update)
        c = 0
        for oficina in user.oficina.all():            
            celula = oficina.choice       
            dados = get_data(setor, context = 'atrasado', oficina = celula)
            if dados['contador'] != 0:     
                text=f"Produção <b>{celula}:</b> {os.linesep}\U00002757 {dados['contador']} entregas EM ATRASO: <b>{dados['somador']} peças.</b>"
                if c == 0:
                    update.edit_message_text(text, parse_mode=ParseMode.HTML)
                    c += 1
                else:
                    update.message.reply_text(text, parse_mode=ParseMode.HTML)
    else:
        dados = get_data(setor, context = 'atrasado') 
        setor = convert_setor(setor)           
        text=f"Produção <b>{setor}:</b> {os.linesep}\U00002757 {dados['contador']} entregas ATRASADAS: <b>{dados['somador']} peças.</b>"
        try:
            update.edit_message_text(text, parse_mode=ParseMode.HTML)
        except:
            update.message.reply_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)
    

def producao_parada(update, setor):
    dados = get_data(setor, context = 'parado')
    setor = convert_setor(setor)
    text=f"Produção <b>{setor}:</b> {os.linesep}\U00002757 {dados['contador']} produtos PARADOS: <b>{dados['somador']} peças.</b>"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)


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
        userbot = get_user(update)
        text = f"\U0001F4AC Escolha uma opção:"
        dict = {}  
        if userbot.geral:
             dict['Geral']='geral'

        if userbot.oficina.count() > 0:
            dict['Confecção']='confeccao'

        if userbot.lavanderia:
             dict['Lavanderia']='lavanderia'
        
        if userbot.expedicao:
             dict['Expedição']='expedicao'

        keyboard = []
        for key, value in dict.items():
            keyboard.append(
            [InlineKeyboardButton(key, callback_data = value)]
            )                
        reply_markup = InlineKeyboardMarkup(keyboard)

        if context == 'nav':
            return keyboard
        else:
            update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

    except:
        p = UserBot(user_id = chat_id, user_nome = first_name)
        p.save() 
        text = f'Olá {first_name}!{os.linesep}Obrigado por acessar nosso sistema.{os.linesep}Já já seu acesso será liberado.'   
        update.message.reply_text(text)    


def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    
    query.answer()
    if query.data == 'geral':
        keyboard = [
        [
            InlineKeyboardButton("Produção em Atraso", callback_data='atraso_geral'),
            InlineKeyboardButton("Produtos Parados", callback_data='parado_geral')
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]
    elif query.data == 'lavanderia':
        keyboard = [
        [
            InlineKeyboardButton("Atraso na Entrega", callback_data='atraso_geral_lavanderia'),
            InlineKeyboardButton("Atraso no Setor", callback_data='menu'),
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]
        
    elif query.data == 'confeccao':
        keyboard = [
        [
            InlineKeyboardButton("Entregas Atrasadas", callback_data='atraso_geral_confeccao'),
            InlineKeyboardButton("Produtos por Oficina", callback_data='menu'),            
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]

    elif query.data == 'expedicao':
        keyboard = [
        [
            InlineKeyboardButton("Entregas Atrasadas", callback_data='atraso_geral_expedicao'),
            InlineKeyboardButton("Produtos Parados", callback_data='menu'),
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]

    elif query.data == 'menu':
        keyboard = menu(query, 'nav')

    elif query.data == 'atraso_geral':        
        return producao_em_atraso(query,12)
    
    elif query.data == 'atraso_geral_confeccao':        
        return producao_em_atraso(query,5)    
    
    elif query.data == 'atraso_geral_lavanderia':        
        return producao_em_atraso(query,7)
    
    elif query.data == 'atraso_geral_expedicao':        
        return producao_em_atraso(query,10)

    elif query.data == 'parado_geral':        
        return producao_parada(query,12)

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('\U0001F4AC escolha uma opção:', reply_markup=reply_markup, parse_mode=ParseMode.HTML)


def resumo_diario(context: CallbackContext):
    from core.models import UserBot
    users = UserBot.objects.all()
    for user in users:        
        resumo = 0
        chat_id = user.user_id
        text=f"""\U00002709 Bom dia, {user.user_nome}! {os.linesep}
        Segue relatório de produção em atraso:{os.linesep}{os.linesep}"""
                 
        if user.geral:
            dados = get_data(12, 'atrasado')
            if dados['contador'] != 0:
                resumo = 1
                setor = "GERAL"
                text += f"""\U00002757<b>{setor}: {os.linesep}
                {dados['contador']} </b>lotes: <b>{dados['somador']} peças.</b>{os.linesep}{os.linesep}"""
                
        if user.oficina.count() > 0:
            dados = get_data(5, 'atrasado')
            if dados['contador'] != 0:
                resumo = 1
                setor = "CONFECÇÃO"
                text += f"""\U00002757<b>{setor}: {os.linesep}
                {dados['contador']} </b>lotes: <b>{dados['somador']} peças.</b>{os.linesep}{os.linesep}"""
                
        if user.lavanderia:
            dados = get_data(7, 'atrasado')
            if dados['contador'] != 0:
                resumo = 1
                setor = "LAVANDERIA"
                text += f"""\U00002757<b>{setor}: {os.linesep}
                {dados['contador']} </b>lotes: <b>{dados['somador']} peças.</b>{os.linesep}{os.linesep}"""

        if user.expedicao:
            dados = get_data(10, 'atrasado')
            if dados['contador'] != 0:
                resumo = 1
                setor = "EXPEDIÇÃO"
                text += f"""\U00002757<b>{setor}: {os.linesep}
                {dados['contador']} </b>lotes: <b>{dados['somador']} peças.</b>{os.linesep}{os.linesep}"""
                
        if resumo == 0:
            text  += f"tudo certo!!!{os.linesep}"
        
        context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)

        keyboard = [[InlineKeyboardButton("Menu", callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text= f"\U0001F4AC para mais informações:"    
        context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

def main() -> None:
        
    
    updater = Updater("1852462745:AAF02s1SOqvgZlfxlLX8iFb_uzhgrY5T8cM")    
    updater.dispatcher.add_handler(MessageHandler(Filters.text, menu))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    hora = datetime.time(0, 3, 00, 000000) # +3 horas
    up_job = updater.job_queue    
    up_job.run_daily(resumo_diario, time=hora, days=(0, 1, 2, 3, 4))    
    #up_job.run_once(resumo_diario, 10)
    updater.start_polling()
    updater.idle()
   

def iniciar():
    from core.models import Bot
    ativo= Bot.objects.latest('token').ativo            
    if ativo:
        return main()   


if __name__ == '__main__':
    main()
