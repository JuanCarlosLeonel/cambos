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
from frota.models import Abastecimento, EstoqueDiesel, FrotaBot, ItemViagem, SolicitacaoViagem, Veiculo, Viagem


def solicitacao1719vermelho(update):
    user = get_user(update)
    viagem = Viagem.objects.filter(veiculo__id = 7, km_final=None)
    item = ItemViagem.objects.filter(viagem__in = viagem, viagem_solicitacao__data_finalizacao = None )
    text =f"<b>Solicitações em Atendimento:</b>{os.linesep}"
    if user.ativo:
        for solicitacao in item:
            if solicitacao.viagem_solicitacao.tipo == '1':
                text += f"Endereço da COLETA:{os.linesep}"
            elif solicitacao.viagem_solicitacao.tipo == '2':
                text += f"Endereço da ENTREGA:{os.linesep}"
            elif solicitacao.viagem_solicitacao.tipo == '3':
                text += f"Endereço da COLETA DIRETA:{os.linesep}"
            elif solicitacao.viagem_solicitacao.tipo == '4':
                text += f"Endereço da ENTRADA DIRETA:{os.linesep}"
            text += f"<b>Rua</b> {solicitacao.viagem_solicitacao.endereco.endereco}{os.linesep}"
            text += f"<b>N</b> {solicitacao.viagem_solicitacao.endereco.numero}{os.linesep}"
            text += f"<b>Bairro</b> {solicitacao.viagem_solicitacao.endereco.bairro}{os.linesep}"
            text += f"<b>Cidade</b> {solicitacao.viagem_solicitacao.endereco.cidade}{os.linesep}"
            text += f"<b>Cep</b> {solicitacao.viagem_solicitacao.endereco.cep}{os.linesep}"
            text += f"<b>Para finalizar a solicitacao</b> : http://192.168.0.90:8000/frota/solicitacaomotorista_update/{solicitacao.viagem_solicitacao.pk}{os.linesep}"
            text += f"============================{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)


def solicitacao1719azul(update):
    user = get_user(update)
    viagem = Viagem.objects.filter(veiculo__id = 6, km_final=None)
    item = ItemViagem.objects.filter(viagem__in = viagem, viagem_solicitacao__data_finalizacao = None )
    text =f"<b>Solicitações em Atendimento:</b>{os.linesep}"
    if user.ativo:
        for solicitacao in item:
            if solicitacao.viagem_solicitacao.tipo == '1':
                text += f"Endereço da COLETA:{os.linesep}"
            elif solicitacao.viagem_solicitacao.tipo == '2':
                text += f"Endereço da ENTREGA:{os.linesep}"
            elif solicitacao.viagem_solicitacao.tipo == '3':
                text += f"Endereço da COLETA DIRETA:{os.linesep}"
            elif solicitacao.viagem_solicitacao.tipo == '4':
                text += f"Endereço da ENTRADA DIRETA:{os.linesep}"
            text += f"<b>Rua</b> {solicitacao.viagem_solicitacao.endereco.endereco}{os.linesep}"
            text += f"<b>N</b> {solicitacao.viagem_solicitacao.endereco.numero}{os.linesep}"
            text += f"<b>Bairro</b> {solicitacao.viagem_solicitacao.endereco.bairro}{os.linesep}"
            text += f"<b>Cidade</b> {solicitacao.viagem_solicitacao.endereco.cidade}{os.linesep}"
            text += f"<b>Cep</b> {solicitacao.viagem_solicitacao.endereco.cep}{os.linesep}"
            text += f"<b>Para finalizar a solicitacao</b> : http://192.168.0.90:8000/frota/solicitacaomotorista_update/{solicitacao.viagem_solicitacao.pk}{os.linesep}"
            text += f"============================{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def solicitacao2426vermelho(update):
    user = get_user(update)
    viagem = Viagem.objects.filter(veiculo__id = 2, km_final=None)
    item = ItemViagem.objects.filter(viagem__in = viagem, viagem_solicitacao__data_finalizacao = None )
    text =f"<b>Solicitações em Atendimento:</b>{os.linesep}"
    if user.ativo:
        for solicitacao in item:
            if solicitacao.viagem_solicitacao.tipo == '1':
                text += f"Endereço da COLETA:{os.linesep}"
            elif solicitacao.viagem_solicitacao.tipo == '2':
                text += f"Endereço da ENTREGA:{os.linesep}"
            elif solicitacao.viagem_solicitacao.tipo == '3':
                text += f"Endereço da COLETA DIRETA:{os.linesep}"
            elif solicitacao.viagem_solicitacao.tipo == '4':
                text += f"Endereço da ENTRADA DIRETA:{os.linesep}"
            text += f"<b>Rua</b> {solicitacao.viagem_solicitacao.endereco.endereco}{os.linesep}"
            text += f"<b>N</b> {solicitacao.viagem_solicitacao.endereco.numero}{os.linesep}"
            text += f"<b>Bairro</b> {solicitacao.viagem_solicitacao.endereco.bairro}{os.linesep}"
            text += f"<b>Cidade</b> {solicitacao.viagem_solicitacao.endereco.cidade}{os.linesep}"
            text += f"<b>Cep</b> {solicitacao.viagem_solicitacao.endereco.cep}{os.linesep}"
            text += f"<b>Para finalizar a solicitacao</b> : http://192.168.0.90:8000/frota/solicitacaomotorista_update/{solicitacao.viagem_solicitacao.pk}{os.linesep}"
            text += f"============================{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def solicitacao24280cinza(update):
    user = get_user(update)
    viagem = Viagem.objects.filter(veiculo__id = 1, km_final=None)
    item = ItemViagem.objects.filter(viagem__in = viagem, viagem_solicitacao__data_finalizacao = None )
    text =f"<b>Solicitações em Atendimento:</b>{os.linesep}"
    if user.ativo:
        for solicitacao in item:
            if solicitacao.viagem_solicitacao.tipo == '1':
                text += f"Endereço da COLETA:{os.linesep}"
            elif solicitacao.viagem_solicitacao.tipo == '2':
                text += f"Endereço da ENTREGA:{os.linesep}"
            elif solicitacao.viagem_solicitacao.tipo == '3':
                text += f"Endereço da COLETA DIRETA:{os.linesep}"
            elif solicitacao.viagem_solicitacao.tipo == '4':
                text += f"Endereço da ENTRADA DIRETA:{os.linesep}"
            text += f"<b>Rua</b> {solicitacao.viagem_solicitacao.endereco.endereco}{os.linesep}"
            text += f"<b>N</b> {solicitacao.viagem_solicitacao.endereco.numero}{os.linesep}"
            text += f"<b>Bairro</b> {solicitacao.viagem_solicitacao.endereco.bairro}{os.linesep}"
            text += f"<b>Cidade</b> {solicitacao.viagem_solicitacao.endereco.cidade}{os.linesep}"
            text += f"<b>Cep</b> {solicitacao.viagem_solicitacao.endereco.cep}{os.linesep}"
            text += f"<b>Para finalizar a solicitacao</b> : http://192.168.0.90:8000/frota/solicitacaomotorista_update/{solicitacao.viagem_solicitacao.pk}{os.linesep}"
            text += f"============================{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def solicitacoes(update):
    user = get_user(update)
    s = SolicitacaoViagem.objects.filter(situacao = 1)
    text =""
    if user.ativo:
        text = f"<b>Solicitações Abertas:</b>{os.linesep}"
        for item in s:
            if item.prioridade == '1':
                text += f"<b>Solicitante:{item.user}</b>{os.linesep}    Prioridade:NORMAL,data{str(item.data_solicitacao)[8:10] + '/' + str(item.data_solicitacao)[5:7] + '/' + str(item.data_solicitacao)[0:4] + '-' + str(item.data_solicitacao)[11:16]}{os.linesep}"
            elif item.prioridade == '2':
                text += f"<b>Solicitante:{item.user}</b>{os.linesep}    Prioridade:NORMAL,data{str(item.data_solicitacao)[8:10] + '/' + str(item.data_solicitacao)[5:7] + '/' + str(item.data_solicitacao)[0:4] + '-' + str(item.data_solicitacao)[11:16]}{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def dieselinterno(update):
    user = get_user(update)
    interno = EstoqueDiesel.objects.get(produto_id = 146)
    text =""
    if user.ativo:
        text = f"Total Disponível:{os.linesep}"
        text += f"<b>{interno.quantidade} l</b>.{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def abastecimento(update):
    from datetime import timedelta
    from datetime import date
    user = get_user(update)
    a = Abastecimento.objects.all()
    text =""
    totgasolina = 0
    totalcool = 0
    totgastogasolina = 0
    totgastoalcool = 0
    totinterno = 0
    totexterno = 0
    totgastointerno = 0
    totgastoexterno = 0
    if user.ativo:
        text = f"<b>Relatório Abastecimento últimos 30 dias</b>:{os.linesep}"
        for item in a:
            if item.data > date.today() - timedelta(days = 30):
                if item.combustivel == 'Gasolina':
                    totgasolina += item.quantidade
                    totgastogasolina += item.valor_unitario
                elif item.combustivel == 'Álcool':
                    totalcool += item.quantidade
                    totgastoalcool += item.valor_unitario
                elif item.combustivel == 'Diesel':
                    if item.interno:
                        totinterno += item.quantidade
                        totgastointerno += item.valor_unitario
                    elif not item.interno:
                        totexterno += item.quantidade
                        totgastoexterno += item.valor_unitario
        text += f"<b>Gasolina: {str(totgasolina)[:5]}</b> l consumidos{os.linesep}   Valor total <b> R$ {totgastogasolina}</b>{os.linesep}<b>Álcool: {str(totalcool)[:5]}</b> l consumidos{os.linesep}   Valor total <b> R$ {totgastoalcool}</b>{os.linesep}<b>Diesel INTERNO: {str(totinterno)[:5]}</b> l consumidos{os.linesep}   Valor total <b> R$ {totgastointerno}</b>{os.linesep}<b>Diesel EXTERNO: {str(totexterno)[:5]}</b> l consumidos{os.linesep}   Valor total <b> R$ {totgastoexterno}</b>{os.linesep}"
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
    if user.ativo:
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
        text += f"<b>Relatório dos últimos 30 dias:{os.linesep}{d} </b>viagens feitas.{os.linesep}Com <b>{cont}</b> km rodados{os.linesep}Consumo de <b>{str(totgasolina)[:5]}</b>l de gasolina{os.linesep}E <b>{str(totalcool)[:5]}</b>l de álcool.{os.linesep}Valor total gasolina <b>R${totgastogasolina}</b>{os.linesep}Valor total álcool <b>R${totgastoalcool}</b>{os.linesep}"
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
    if user.ativo:
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
        text += f"<b>Relatório dos últimos 30 dias:{os.linesep}{d} </b>viagens feitas.{os.linesep}Com <b>{cont}</b> km rodados{os.linesep}Consumo de <b>{str(totgasolina)[:5]}</b>l de gasolina{os.linesep}E <b>{str(totalcool)[:5]}</b>l de álcool.{os.linesep}Valor total gasolina <b>R${totgastogasolina}</b>{os.linesep}Valor total álcool <b>R${totgastoalcool}</b>{os.linesep}"
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
    if user.ativo:
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
        text += f"<b>Relatório dos últimos 30 dias:{os.linesep}{d} </b>viagens feitas.{os.linesep}Com <b>{cont}</b> km rodados{os.linesep}Consumo de <b>{str(totgasolina)[:5]}</b>l de gasolina{os.linesep}E <b>{str(totalcool)[:5]}</b>l de álcool.{os.linesep}Valor total gasolina <b>R${totgastogasolina}</b>{os.linesep}Valor total álcool <b>R${totgastoalcool}</b>{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def MB1719Vermelho(update):
    from datetime import timedelta
    from datetime import date
    user = get_user(update)
    veiculo = Veiculo.objects.filter(id = 7)
    viagem = Viagem.objects.filter(veiculo__in = veiculo)
    abastecimento = Abastecimento.objects.filter(veiculo__in = veiculo)
    text =""
    cont = 0
    d = 0
    totdieselinterno = 0
    totdieselexterno = 0
    totgastointerno = 0
    totgastoexterno = 0
    if user.ativo:
        text = f"<b>Caminhão MB 1719 Vermelho</b>:{os.linesep}"
        for item in viagem:
            if item.data_inicial > date.today() - timedelta(days = 30):
                d += 1
                if item.km_final is None:
                    pass
                else:
                    cont += (item.km_final - item.km_inicial)
        for abas in abastecimento:
            if abas.data > date.today() - timedelta(days = 30):
                if abas.interno:
                    totdieselinterno += abas.quantidade
                    totgastointerno += abas.valor_unitario
                elif not abas.interno:
                    totdieselexterno += abas.quantidade
                    totgastoexterno += abas.valor_unitario
        text += f"<b>Relatório dos últimos 30 dias:{os.linesep}{d} </b>viagens feitas.{os.linesep}Com <b>{cont}</b> km rodados{os.linesep}Consumo: <b>{str(totdieselinterno)[:5]}</b>l de diesel INTERNO{os.linesep}E <b>{str(totdieselexterno)[:5]}</b>l de diesel EXTERNO{os.linesep}Valor total INTERNO <b>R${totgastointerno}</b>{os.linesep}Valor total EXTERNO <b>R${totgastoexterno}</b>{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def MB1719Azul(update):
    from datetime import timedelta
    from datetime import date
    user = get_user(update)
    veiculo = Veiculo.objects.filter(id = 6)
    viagem = Viagem.objects.filter(veiculo__in = veiculo)
    abastecimento = Abastecimento.objects.filter(veiculo__in = veiculo)
    text =""
    cont = 0
    d = 0
    totdieselinterno = 0
    totdieselexterno = 0
    totgastointerno = 0
    totgastoexterno = 0
    if user.ativo:
        text = f"<b>Caminhão MB 1719 Azul</b>:{os.linesep}"
        for item in viagem:
            if item.data_inicial > date.today() - timedelta(days = 30):
                d += 1
                if item.km_final is None:
                    pass
                else:
                    cont += (item.km_final - item.km_inicial)
        for abas in abastecimento:
            if abas.data > date.today() - timedelta(days = 30):
                if abas.interno:
                    totdieselinterno += abas.quantidade
                    totgastointerno += abas.valor_unitario
                elif not abas.interno:
                    totdieselexterno += abas.quantidade
                    totgastoexterno += abas.valor_unitario
        text += f"<b>Relatório dos últimos 30 dias:{os.linesep}{d} </b>viagens feitas.{os.linesep}Com <b>{cont}</b> km rodados{os.linesep}Consumo: <b>{str(totdieselinterno)[:5]}</b>l de diesel INTERNO{os.linesep}E <b>{str(totdieselexterno)[:5]}</b>l de diesel EXTERNO{os.linesep}Valor total INTERNO <b>R${totgastointerno}</b>{os.linesep}Valor total EXTERNO <b>R${totgastoexterno}</b>{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def MB2426Vermelho(update):
    from datetime import timedelta
    from datetime import date
    user = get_user(update)
    veiculo = Veiculo.objects.filter(id = 2)
    viagem = Viagem.objects.filter(veiculo__in = veiculo)
    abastecimento = Abastecimento.objects.filter(veiculo__in = veiculo)
    text =""
    cont = 0
    d = 0
    totdieselinterno = 0
    totdieselexterno = 0
    totgastointerno = 0
    totgastoexterno = 0
    if user.ativo:
        text = f"<b>Caminhão MB 2426 Vermelho</b>:{os.linesep}"
        for item in viagem:
            if item.data_inicial > date.today() - timedelta(days = 30):
                d += 1
                if item.km_final is None:
                    pass
                else:
                    cont += (item.km_final - item.km_inicial)
        for abas in abastecimento:
            if abas.data > date.today() - timedelta(days = 30):
                if abas.interno:
                    totdieselinterno += abas.quantidade
                    totgastointerno += abas.valor_unitario
                elif not abas.interno:
                    totdieselexterno += abas.quantidade
                    totgastoexterno += abas.valor_unitario
        text += f"<b>Relatório dos últimos 30 dias:{os.linesep}{d} </b>viagens feitas.{os.linesep}Com <b>{cont}</b> km rodados{os.linesep}Consumo: <b>{str(totdieselinterno)[:5]}</b>l de diesel INTERNO{os.linesep}E <b>{str(totdieselexterno)[:5]}</b>l de diesel EXTERNO{os.linesep}Valor total INTERNO <b>R${totgastointerno}</b>{os.linesep}Valor total EXTERNO <b>R${totgastoexterno}</b>{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def VW24280Cinza(update):
    from datetime import timedelta
    from datetime import date
    user = get_user(update)
    veiculo = Veiculo.objects.filter(id = 1)
    viagem = Viagem.objects.filter(veiculo__in = veiculo)
    abastecimento = Abastecimento.objects.filter(veiculo__in = veiculo)
    text =""
    cont = 0
    d = 0
    totdieselinterno = 0
    totdieselexterno = 0
    totgastointerno = 0
    totgastoexterno = 0
    if user.ativo:
        text = f"<b>Caminhão VW 24280 Cinza</b>:{os.linesep}"
        for item in viagem:
            if item.data_inicial > date.today() - timedelta(days = 30):
                d += 1
                if item.km_final is None:
                    pass
                else:
                    cont += (item.km_final - item.km_inicial)
        for abas in abastecimento:
            if abas.data > date.today() - timedelta(days = 30):
                if abas.interno:
                    totdieselinterno += abas.quantidade
                    totgastointerno += abas.valor_unitario
                elif not abas.interno:
                    totdieselexterno += abas.quantidade
                    totgastoexterno += abas.valor_unitario
        text += f"<b>Relatório dos últimos 30 dias:{os.linesep}{d} </b>viagens feitas.{os.linesep}Com <b>{cont}</b> km rodados{os.linesep}Consumo: <b>{str(totdieselinterno)[:5]}</b>l de diesel INTERNO{os.linesep}E <b>{str(totdieselexterno)[:5]}</b>l de diesel EXTERNO{os.linesep}Valor total INTERNO <b>R${totgastointerno}</b>{os.linesep}Valor total EXTERNO <b>R${totgastoexterno}</b>{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)


def get_user(update):
    from frota.models import FrotaBot
    user_id = update.message.chat_id
    userbot = FrotaBot.objects.get(user_id = user_id)
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
    chat_id = update.message.chat_id    
    first_name = update.message.chat.first_name
    try:
        userbot = get_user(update)
        text = f"\U0001F4AC Escolha uma opção:"
        dict = {}  
        if userbot:
            dict['\U0001F4CB Logística']='frota'
            dict['\U0001F68C Veículos']='veiculo'
            dict['\U0001F69A Viagens']='viagemsolicitacao'

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
        p = FrotaBot(user_id = chat_id, user_nome = first_name)
        p.save() 
        text = f'Olá {first_name}!{os.linesep}Obrigado por acessar nosso sistema.{os.linesep}Já já seu acesso será liberado.'   
        update.message.reply_text(text)    

def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    
    query.answer()
    if query.data == 'frota':
        keyboard = [
        [
            InlineKeyboardButton("\U0001F4CB Solicitações", callback_data='solicitacoes'),
            InlineKeyboardButton("\U0000203C Em atendimento", callback_data='solicitacao1719vermelho'),
        ],
        [   InlineKeyboardButton("\U000026FD Abastecimento", callback_data='abastecimento'),
            InlineKeyboardButton("\U000026FD Diesel Interno", callback_data='dieselinterno'),
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]

    if query.data == 'viagemsolicitacao':
        keyboard = [
        [
            InlineKeyboardButton("\U0001F69A 1719 Azul", callback_data='solicitacao1719azul'),
            InlineKeyboardButton("\U0001F69A 1719 Vermelho", callback_data='solicitacao1719vermelho'),
        ],
        [   InlineKeyboardButton("\U0001F69A 2426 Vermelho", callback_data='solicitacao2426vermelho'),
            InlineKeyboardButton("\U0001F69A 24280 Cinza", callback_data='solicitacao24280cinza'),
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

    elif query.data == 'solicitacoes':
        return solicitacoes(query)

    elif query.data == 'solicitacao1719vermelho':
        return solicitacao1719vermelho(query)

    elif query.data == 'solicitacao1719azul':
        return solicitacao1719azul(query)

    elif query.data == 'solicitacao2426vermelho':
        return solicitacao2426vermelho(query)
    
    elif query.data == 'solicitacao24280cinza':
        return solicitacao24280cinza(query)

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
    bot = Bot.objects.get(nome = 'Frota')
    token = bot.token
    updater = Updater(token)   
    updater.dispatcher.add_handler(MessageHandler(Filters.text, start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

def iniciar():
    from core.models import Bot
    ativo= Bot.objects.get(nome = 'Frota').ativo            
    if ativo:
        return main()  
      
if __name__ == '__main__':
    main()