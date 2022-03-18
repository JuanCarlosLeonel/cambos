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
from frota.models import Abastecimento, EstoqueDiesel, Veiculo, Viagem

def viagemcaminhao(update):
    user = get_user(update)
    v = Viagem.objects.filter(veiculo__caminhao = True)
    text =""
    if user.frota:
        text = f"\U00002757Viagens <b>EM TRÂNSITO</b>:{os.linesep}"
        for item in v:
            if item.data_final is None:
                text += f"<b>{item.veiculo}</b>, saída:{str(item.data_inicial)[8:] + '/' + str(item.data_inicial)[5:7] + '/' + str(item.data_inicial)[0:4] }, destino:{item.destino}{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def dieselinterno(update):
    user = get_user(update)
    interno = EstoqueDiesel.objects.get(produto_id = 146)
    text =""
    if user.frota:
        text = f"Total Disponível:{os.linesep}"
        text += f"<b>{interno.quantidade} l</b>.{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def abastecimento(update):
    user = get_user(update)
    a = Abastecimento.objects.filter(veiculo__caminhao = True).order_by("-id")
    text =""
    if user.frota:
        text = f"Abastecimentos Realizados:{os.linesep}"
        for item in a:
            text += f"<b>{item.veiculo}</b>, {str(item.data)[8:] + '/' + str(item.data)[5:7] + '/' + str(item.data)[0:4]}{os.linesep} Combustível:<i>{item.combustivel}</i>, Valor pago:{item.valor_unitario}.{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def palio(update):
    from datetime import timedelta
    from datetime import date
    user = get_user(update)
    veiculo = Veiculo.objects.filter(id = 3)
    viagem = Viagem.objects.filter(veiculo__in = veiculo)
    abastecimento = Abastecimento.objects.filter(veiculo__in = veiculo)
    text =""
    cont = 0
    d = 0
    totgasolina = 0
    totalcool = 0
    totgastogasolina = 0
    totgastoalcool = 0
    if user.frota:
        text = f"<b>Fiat Palio</b>:{os.linesep}"
        for item in viagem:
            if item.data_inicial > date.today() - timedelta(days = 30):
                d += 1
                if item.km_final is None:
                    pass
                else:
                    cont += (item.km_final - item.km_inicial)
        for abas in abastecimento:
            if abas.data > date.today() - timedelta(days = 30):
                if abas.combustivel == 'Gasolina':
                    totgasolina += abas.quantidade
                    totgastogasolina += abas.valor_unitario
                elif abas.combustivel == 'Álcool':
                    totalcool += abas.quantidade
                    totalcool += abas.valor_unitario
        text += f"<b>{d} </b>viagens nos últimos 30 dias.{os.linesep}Com <b>{cont}</b> km rodados{os.linesep}Consumo de <b>{str(totgasolina)[:5]}</b>l de gasolina{os.linesep}E <b>{str(totalcool)[:5]}</b>l de álcool.{os.linesep}Valor total gasolina <b>{totgastogasolina}</b>{os.linesep}Valor total álcool <b>{totgastoalcool}</b>{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def mobi(update):
    from datetime import timedelta
    from datetime import date
    user = get_user(update)
    veiculo = Veiculo.objects.filter(id = 4)
    viagem = Viagem.objects.filter(veiculo__in = veiculo)
    abastecimento = Abastecimento.objects.filter(veiculo__in = veiculo)
    text =""
    cont = 0
    d = 0
    totgasolina = 0
    totalcool = 0
    totgastogasolina = 0
    totgastoalcool = 0
    if user.frota:
        text = f"<b>Fiat Mobi</b>:{os.linesep}"
        for item in viagem:
            if item.data_inicial > date.today() - timedelta(days = 30):
                d += 1
                if item.km_final is None:
                    pass
                else:
                    cont += (item.km_final - item.km_inicial)
        for abas in abastecimento:
            if abas.data > date.today() - timedelta(days = 30):
                if abas.combustivel == 'Gasolina':
                    totgasolina += abas.quantidade
                    totgastogasolina += abas.valor_unitario
                elif abas.combustivel == 'Álcool':
                    totalcool += abas.quantidade
                    totalcool += abas.valor_unitario
        text += f"<b>{d} </b>viagens nos últimos 30 dias.{os.linesep}Com <b>{cont}</b> km rodados{os.linesep}Consumo de <b>{str(totgasolina)[:5]}</b>l de gasolina{os.linesep}E <b>{str(totalcool)[:5]}</b>l de álcool.{os.linesep}Valor total gasolina <b>{totgastogasolina}</b>{os.linesep}Valor total álcool <b>{totgastoalcool}</b>{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def strada(update):
    from datetime import timedelta
    from datetime import date
    user = get_user(update)
    veiculo = Veiculo.objects.filter(id = 5)
    viagem = Viagem.objects.filter(veiculo__in = veiculo)
    abastecimento = Abastecimento.objects.filter(veiculo__in = veiculo)
    text =""
    cont = 0
    d = 0
    totgasolina = 0
    totalcool = 0
    totgastogasolina = 0
    totgastoalcool = 0
    if user.frota:
        text = f"<b>Fiat Strada</b>:{os.linesep}"
        for item in viagem:
            if item.data_inicial > date.today() - timedelta(days = 30):
                d += 1
                if item.km_final is None:
                    pass
                else:
                    cont += (item.km_final - item.km_inicial)
        for abas in abastecimento:
            if abas.data > date.today() - timedelta(days = 30):
                if abas.combustivel == 'Gasolina':
                    totgasolina += abas.quantidade
                    totgastogasolina += abas.valor_unitario
                elif abas.combustivel == 'Álcool':
                    totalcool += abas.quantidade
                    totalcool += abas.valor_unitario
        text += f"<b>{d} </b>viagens nos últimos 30 dias.{os.linesep}Com <b>{cont}</b> km rodados{os.linesep}Consumo de <b>{str(totgasolina)[:5]}</b>l de gasolina{os.linesep}E <b>{str(totalcool)[:5]}</b>l de álcool.{os.linesep}Valor total gasolina <b>{totgastogasolina}</b>{os.linesep}Valor total álcool <b>{totgastoalcool}</b>{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def MB1719Vermelho(update):
    from datetime import timedelta
    from datetime import date
    user = get_user(update)
    veiculo = Veiculo.objects.filter(id = 7)
    viagem = Viagem.objects.filter(veiculo__in = veiculo)
    text =""
    cont = 0
    d = 0
    if user.frota:
        text = f"<b>Caminhão MB 1719 Vermelho</b>:{os.linesep}"
        for item in viagem:
            if item.data_inicial > date.today() - timedelta(days = 30):
                d += 1
                if item.km_final is None:
                    pass
                else:
                    cont += (item.km_final - item.km_inicial)
        text += f"<b>{d} </b>viagens nos últimos 30 dias.{os.linesep} Com <b>{cont}</b> km rodados{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def MB1719Azul(update):
    from datetime import timedelta
    from datetime import date
    user = get_user(update)
    veiculo = Veiculo.objects.filter(id = 6)
    viagem = Viagem.objects.filter(veiculo__in = veiculo)
    text =""
    cont = 0
    d = 0
    if user.frota:
        text = f"<b>Caminhão MB 1719 Azul</b>:{os.linesep}"
        for item in viagem:
            if item.data_inicial > date.today() - timedelta(days = 30):
                d += 1
                if item.km_final is None:
                    pass
                else:
                    cont += (item.km_final - item.km_inicial)
        text += f"<b>{d} </b>viagens nos últimos 30 dias.{os.linesep} Com <b>{cont}</b> km rodados{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def MB2426Vermelho(update):
    from datetime import timedelta
    from datetime import date
    user = get_user(update)
    veiculo = Veiculo.objects.filter(id = 2)
    viagem = Viagem.objects.filter(veiculo__in = veiculo)
    text =""
    cont = 0
    d = 0
    if user.frota:
        text = f"<b>Caminhão MB 2426 Vermelho</b>:{os.linesep}"
        for item in viagem:
            if item.data_inicial > date.today() - timedelta(days = 30):
                d += 1
                if item.km_final is None:
                    pass
                else:
                    cont += (item.km_final - item.km_inicial)
        text += f"<b>{d} </b>viagens nos últimos 30 dias.{os.linesep} Com <b>{cont}</b> km rodados{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def VW24280Cinza(update):
    from datetime import timedelta
    from datetime import date
    user = get_user(update)
    veiculo = Veiculo.objects.filter(id = 1)
    viagem = Viagem.objects.filter(veiculo__in = veiculo)
    text =""
    cont = 0
    d = 0
    if user.frota:
        text = f"<b>Caminhão VW 24280 Cinza</b>:{os.linesep}"
        for item in viagem:
            if item.data_inicial > date.today() - timedelta(days = 30):
                d += 1
                if item.km_final is None:
                    pass
                else:
                    cont += (item.km_final - item.km_inicial)
        text += f"<b>{d} </b>viagens nos últimos 30 dias.{os.linesep} Com <b>{cont}</b> km rodados{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def get_user(update):
    from roupa.models import RoupaBot
    user_id = update.message.chat_id
    userbot = RoupaBot.objects.get(user_id = user_id)
    return userbot
                
           
def return_menu(update, text):
    keyboard = [[InlineKeyboardButton(f'\U000021A9 Menu', callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)    
    update.message.reply_text('\U0001F698', reply_markup=reply_markup)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def menu(update, context):
    from roupa.models import RoupaBot, User
    chat_id = update.message.chat_id    
    first_name = update.message.chat.first_name
    mensagem = update.message.text  
    try:
        userbot = get_user(update)
        text = f"\U0001F4AC Escolha uma opção:"
        dict = {}  
        if userbot.frota:
            dict['\U0001F4CB Logística']='frota'
            dict['\U0001F68C Veículo']='veiculo'

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
        p = RoupaBot(user_id = chat_id, user_nome = first_name)
        p.save() 
        text = f'Olá {first_name}!{os.linesep}Obrigado por acessar nosso sistema.{os.linesep}Já já seu acesso será liberado.'   
        update.message.reply_text(text)    

def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    
    query.answer()
    if query.data == 'frota':
        keyboard = [
        [
            InlineKeyboardButton("\U0001F4CB Solicitações", callback_data='menu'),
            InlineKeyboardButton("\U0000203C Em trânsito", callback_data='viagemcaminhao'),
        ],
        [   InlineKeyboardButton("\U000026FD Abastecimento", callback_data='abastecimento'),
        InlineKeyboardButton("\U000026FD Diesel Interno", callback_data='dieselinterno'),
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]

    if query.data == 'veiculo':
        keyboard = [
        [
            InlineKeyboardButton("\U0001F697 Fiat Palio", callback_data='palio'),
            InlineKeyboardButton("\U0001F697 Fiat Strada", callback_data='strada'),
            InlineKeyboardButton("\U0001F697 Fiat Mobi", callback_data='mobi'),
        ],
        [   InlineKeyboardButton("\U0001F69A MB 1719 Vermelho", callback_data='MB1719Vermelho'),
            InlineKeyboardButton("\U0001F69A MB 1719 Azul", callback_data='MB1719Azul'),
        ],
        [
            InlineKeyboardButton("\U0001F69A MB 2426 Vermelho", callback_data='MB2426Vermelho'),
            InlineKeyboardButton("\U0001F69A VW 24280 Cinza", callback_data='VW24280Cinza'),
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]

    elif query.data == 'menu':
        keyboard = menu(query, 'nav')

    elif query.data == 'viagemcaminhao':
        return viagemcaminhao(query)

    elif query.data == 'abastecimento':
        return abastecimento(query)

    elif query.data == 'dieselinterno':
        return dieselinterno(query)

    elif query.data == 'palio':
        return palio(query)

    elif query.data == 'strada':
        return strada(query)

    elif query.data == 'mobi':
        return mobi(query)

    elif query.data == 'MB1719Vermelho':
        return MB1719Vermelho(query)

    elif query.data == 'MB1719Azul':
        return MB1719Azul(query)

    elif query.data == 'MB2426Vermelho':
        return MB2426Vermelho(query)

    elif query.data == 'VW24280Cinza':
        return VW24280Cinza(query)

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('\U0001F4AC Escolha uma opção:', reply_markup=reply_markup, parse_mode=ParseMode.HTML)


def start(update, context):
    chat_id = update.message.chat_id
    mensagem = update.message.text
    keyboard = [
        [
            InlineKeyboardButton("Menu", callback_data='menu'),
            InlineKeyboardButton("CAMBOS-BI", url='https://indicador.souzacambos.com.br/'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text= f"\U0001F4AC Escolha uma opção:"    
    context.bot.send_chat_action(chat_id, "typing")
    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


def main() -> None:
    from core.models import Bot
    bot = Bot.objects.filter(id=2).latest('token')
    token = bot.token
    updater = Updater(token)   
    updater.dispatcher.add_handler(MessageHandler(Filters.text, start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

def iniciar():
    from core.models import Bot
    ativo = Bot.objects.filter(id=2).latest('token')     
    if ativo.ativo:
        return main()   
      
if __name__ == '__main__':
    main()