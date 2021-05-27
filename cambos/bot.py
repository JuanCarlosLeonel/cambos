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
from roupa.views import get_url
from dateutil import parser


dados = get_url()
total_pecas = 0
entrega_atraso = 0
quantidade_atraso = 0
produto_parado = 0  
quantidade_parado = 0      
for produto in dados:
    data = parser.parse(produto['DataEntrega'])            
    total_pecas += produto['QuantPecas']
    if produto['Atrasado'] == "Atrasado":
        entrega_atraso += 1
        quantidade_atraso += produto['QuantPecas']
    if produto['Parado'] == "1":
        produto_parado += 1  
        quantidade_parado += produto['QuantPecas']


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
        if userbot.geral:
             dict['Geral']='geral'

        if userbot.oficina.count() > 0:
            dict['Terceirizados']='terceirizados'

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
            update.message.reply_text(text, reply_markup=reply_markup)

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
    if query.data == 'lavanderia':
        keyboard = [
        [
            InlineKeyboardButton("Atraso na Entrega", callback_data='atraso_geral_lavanderia'),
            InlineKeyboardButton("Atraso no Setor", callback_data='menu'),
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]
        
    if query.data == 'terceirizados':
        keyboard = [
        [
            InlineKeyboardButton("Produtos por Oficina", callback_data='menu'),
            InlineKeyboardButton("Entregas Atrasadas", callback_data='menu'),
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]

    if query.data == 'expedicao':
        keyboard = [
        [
            InlineKeyboardButton("Entregas Atrasadas", callback_data='atraso_geral_expedicao'),
            InlineKeyboardButton("Produtos Parados", callback_data='menu'),
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]

    if query.data == 'menu':
        keyboard = menu(query, 'nav')

    if query.data == 'atraso_geral':        
        return producao_em_atraso(query,'geral')
    
    if query.data == 'atraso_geral_lavanderia':        
        return producao_em_atraso(query,7)
    
    if query.data == 'atraso_geral_expedicao':        
        return producao_em_atraso(query,10)

    if query.data == 'parado_geral':        
            return producao_parada(query,'geral')

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('escolha uma opção:', reply_markup=reply_markup)
    
def producao_em_atraso(update, setor):    
    entrega_atraso = 0
    quantidade_atraso = 0    
    for produto in dados:
        if setor == 'geral':                
            if produto['Atrasado'] == "Atrasado":
                entrega_atraso += 1
                quantidade_atraso += produto['QuantPecas']
        else:
            if produto['Status'] == setor:
                if produto['Atrasado'] == "Atrasado":
                    entrega_atraso += 1
                    quantidade_atraso += produto['QuantPecas']
            
    text=f"\U00002757 {entrega_atraso} entregas atrasadas: <b>{quantidade_atraso} peças.</b>"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    

def producao_parada(update, setor):
    text=f"\U00002757 {produto_parado} produtos parados: <b>{quantidade_parado} peças.</b>"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)



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