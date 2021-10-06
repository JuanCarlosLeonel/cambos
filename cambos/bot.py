from roupa.models import UserEtapa
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
from roupa.views import get_url, convert_setor
from dateutil import parser
import datetime

def get_user(update):
    from core.models import UserBot
    user_id = update.message.chat_id
    userbot = UserBot.objects.get(user_id = user_id)
    return userbot

def get_data(setor, context, oficina=None, context2 = None):
    dados = get_url()    
    contador = 0
    somador = 0   
    listaficha = [] 
    listadiascostura = []
    celcostura = []
    dataentrega = []
    for produto in dados:  
        if setor == 12:
            if context == 'atrasado':
                if produto['Atrasado'] == "Atrasado":
                    contador += 1
                    somador += produto['QuantPecas']
                    listaficha.append(produto['FichaCorte'])
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
                                listaficha.append(produto['FichaCorte'])
                                listadiascostura.append(produto['DiasCostura']) 
                            elif produto['DiasCostura'] >= 18:
                                contador += 1
                                somador += produto['QuantPecas']
                                listaficha.append(produto['FichaCorte'])
                                listadiascostura.append(produto['DiasCostura'])
                        elif context == 'emdia':
                            if produto['Atrasado'] == "Em Dia":
                                contador += 1
                                somador += produto['QuantPecas']
                                listaficha.append(produto['FichaCorte'])
                                listadiascostura.append(produto['DiasCostura'])
                        elif context == 'atrasados':
                            if produto['Atrasado'] == "Atrasado":
                                contador += 1
                                somador += produto['QuantPecas']
                                listaficha.append(produto['FichaCorte'])
                                dataentrega.append(produto['DataEntrega'])
                                celcostura.append(produto['Celula'])
                        elif context == 'parado':
                            if produto['Parado'] == "1":
                                contador += 1
                                somador += produto['QuantPecas']
                                listaficha.append(produto['FichaCorte'])
                                celcostura.append(produto['Celula'])
                        elif context == 'tudo':
                            contador += 1
                            somador += produto['QuantPecas']
                            listaficha.append(produto['FichaCorte']) 
                            listadiascostura.append(produto['DiasCostura'])           
                if not context2 is None:
                    for oficina in context2.all():
                        if produto['Celula'] == oficina.nick_spi:
                            if context == 'atrasado':                        
                                if produto['Atrasado'] == "Em Atraso":            
                                    contador += 1
                                    somador += produto['QuantPecas']    
                                    listaficha.append(produto['FichaCorte'])
                                    listadiascostura.append(produto['DiasCostura'])
                                    celcostura.append(produto['Celula'])
                                elif produto['DiasCostura'] >= 18:
                                    contador += 1
                                    somador += produto['QuantPecas']
                                    listaficha.append(produto['FichaCorte'])
                                    listadiascostura.append(produto['DiasCostura'])
                                    celcostura.append(produto['Celula'])
                            elif context == 'emdia':
                                if produto['Atrasado'] == "Em Dia":
                                    contador += 1
                                    somador += produto['QuantPecas']
                                    listaficha.append(produto['FichaCorte'])
                            elif context == 'parado':
                                if produto['Parado'] == "1":
                                    contador += 1
                                    somador += produto['QuantPecas']
                                    listaficha.append(produto['FichaCorte'])
                                    celcostura.append(produto['Celula'])
                if oficina is None and context2 is None:
                    if context == 'atrasado':                        
                        if produto['Atrasado'] == "Em Atraso":            
                            contador += 1
                            somador += produto['QuantPecas']    
                            listaficha.append(produto['FichaCorte'])
                            listadiascostura.append(produto['DiasCostura'])
                            celcostura.append(produto['Celula'])
                        elif produto['DiasCostura>18'] >=18:
                            contador +=1
                            somador += produto['QuantPecas']
                            listaficha.append(produto['FichaCorte'])
                            listadiascostura.append(produto['DiasCostura'])
                            celcostura.append(produto['Celula'])
                    elif context == 'emdia':
                        if produto['Atrasado'] == "Em Dia":
                            contador += 1
                            somador += produto['QuantPecas']
                            listaficha.append(produto['FichaCorte'])
                            celcostura.append(produto['Celula'])
                    elif context == 'parado':
                        if produto['Parado'] == "1":
                            contador += 1
                            somador += produto['QuantPecas']
                            listaficha.append(produto['FichaCorte'])
                            listadiascostura.append(produto['DiasCostura'])
                            celcostura.append(produto['Celula'])
        elif setor == 6:
            if produto['Status'] == setor:
                if context == 'atrasado':                        
                    if produto['Atrasado'] == "Em Atraso":            
                        contador += 1
                        somador += produto['QuantPecas']   
                        listaficha.append(produto['FichaCorte'])
                        listadiascostura.append(produto['DiasCostura']) 
                    elif produto['DiasCostura'] >= 18:
                        contador += 1
                        somador += produto['QuantPecas']
                        listaficha.append(produto['FichaCorte'])
                        listadiascostura.append(produto['DiasCostura'])
                if context =='pecas':
                    contador +=1
                    somador += produto['QuantPecas']
                    listaficha.append(produto['FichaCorte'])
                    listadiascostura.append(produto['DiasCostura'])                     
        else:
            if produto['Status'] == setor:
                if context == 'atrasado':                        
                    if produto['Atrasado'] == "Em Atraso":            
                        contador += 1
                        somador += produto['QuantPecas']  
                        listaficha.append(produto['FichaCorte'])  
                elif context == 'emdia':
                    if produto['Atrasado'] == "Em Dia":
                        contador += 1
                        somador += produto['QuantPecas']
                        listaficha.append(produto['FichaCorte'])
                elif context == 'atrasados':
                    if produto['Atrasado'] == "Atrasado":
                        contador += 1
                        somador += produto['QuantPecas']
                        listaficha.append(produto['FichaCorte'])
                elif context == 'parado':
                    if produto['Parado'] == "1":
                        contador += 1
                        somador += produto['QuantPecas']
                        listaficha.append(produto['FichaCorte'])

    return {'contador':contador,'somador':somador,'listaficha':listaficha,'listadiascostura':listadiascostura,'celcostura':celcostura,'dataentrega':dataentrega}

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
            dados = get_data(setor, context = 'atrasado', oficina = celula, context2=None)
            if dados['contador'] != 0:     
                text=f"Produção <b>{celula}:</b>{os.linesep}\U00002757{dados['contador']} entregas EM ATRASO:<b>{dados['somador']} peças.</b>{os.linesep}"
                for item1,item2 in zip (dados['listaficha'],dados['listadiascostura']):
                    text +=f" <b>\U00002714FC: {item1}, {item2} dias na costura.{os.linesep}</b>"
                if c == 0:
                    update.edit_message_text(text, parse_mode=ParseMode.HTML)
                    c += 1
                else:
                    update.message.reply_text(text, parse_mode=ParseMode.HTML)
        else:
            text = f"nada"
    elif setor == 7:
        dados = get_data(setor, context = 'atrasado') 
        setor = convert_setor(setor)           
        text=f"Produção <b>{setor}:</b>{os.linesep}\U00002757{dados['contador']} entregas EM ATRASO:<b> {dados['somador']} peças.</b>{os.linesep}"
        for item in dados['listaficha']:
            text +=f"<b>\U00002714FC: {item}</b>{os.linesep}"
        try:
            update.edit_message_text(text, parse_mode=ParseMode.HTML)
        except:
            update.message.reply_text(text, parse_mode=ParseMode.HTML)
    else:
        dados = get_data(setor, context = 'atrasado') 
        setor = convert_setor(setor)           
        text=f"Produção <b>{setor}:</b>{os.linesep}\U00002757{dados['contador']} entregas EM ATRASO:<b> {dados['somador']} peças.</b>{os.linesep}"
        try:
            update.edit_message_text(text, parse_mode=ParseMode.HTML)
        except:
            update.message.reply_text(text, parse_mode=ParseMode.HTML)
        
    return return_menu(update, text)

def producao_por_celula(update, setor):            
    if setor == 5:
        user = get_user(update)
        c = 0
        for oficina in user.oficina.all():           
            celula = oficina.choice       
            dados = get_data(setor,context = 'tudo', oficina = celula)
            if dados['contador'] != 0:     
                text=f"Produção <b>{celula}:</b>{os.linesep}\U00002757{dados['contador']} entregas: <b>{dados['somador']} peças.</b>{os.linesep}"
                for item1,item2 in zip (dados['listaficha'],dados['listadiascostura']):
                    text +=f"<b>\U00002714FC: {item1}, {item2} dias na costura.{os.linesep}</b>"
                if c == 0:
                    update.edit_message_text(text, parse_mode=ParseMode.HTML)
                    c += 1
                else:
                    update.message.reply_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def prazos_estourados_confeccao(update, setor):
    if setor == 5:
        user = get_user(update)
        c = 0
        for oficina in user.oficina.all():            
            celula = oficina.choice       
            dados = get_data(setor, context = 'atrasados', oficina = celula, context2=None)
            if dados['contador'] != 0:     
                text=f"Entregas com <b>PRAZO ESTOURADO</b>:{os.linesep}\U00002757{dados['contador']} entregas:<b>{dados['somador']} peças.</b>{os.linesep}"
                for item1,item2,item3 in zip (dados['listaficha'],dados['dataentrega'],dados['celcostura']):
                    text +=f"<b>FC</b>:{item1},<b>DATA</b>:{item2}<b>({item3})</b>{os.linesep}"
                if c == 0:
                    update.edit_message_text(text, parse_mode=ParseMode.HTML)
                    c += 1
                else:
                    update.message.reply_text(text, parse_mode=ParseMode.HTML)
            else:
                text = f"nada"
    return return_menu(update, text)

def producao_parada(update, setor):
    dados = get_data(setor, context = 'parado')
    setor = convert_setor(setor)
    text=f"Produção <b>{setor}:</b> {os.linesep}\U00002757 {dados['contador']} produtos PARADOS: <b>{dados['somador']} peças.</b>{os.linesep}"
    for item in dados['listaficha']:
        text +=f"<b>\U00002714FC: {item}</b>{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def producao_parada_costura(update, setor):
    dados = get_data(setor, context= 'parado')
    setor = convert_setor(setor)
    text=f"Entregas <b>PARADAS</b> no setor:{os.linesep}\U00002757{dados['contador']} entregas: <b>{dados['somador']} peças.</b>{os.linesep}"
    for item1,item2,item3 in zip (dados['listaficha'],dados['listadiascostura'],dados['celcostura']):
        text +=f"<b>FC</b>:{item1},<b>{item2}</b>dias na costura.<b>({item3})</b>{os.linesep}"

    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def produtos_finalizacao(update, setor): 
    dados = get_data(setor, context= 'pecas')
    setor = convert_setor(setor)
    text=f"Produção <b>{setor}:</b>{os.linesep}\U00002757{dados['contador']} produtos no setor: <b>{dados['somador']} peças.</b>{os.linesep}"
    for item1,item2 in zip (dados['listaficha'],dados['listadiascostura']):
        text +=f" <b>\U00002714FC: {item1}, {item2} dias na costura.{os.linesep}</b>"

    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def atrasados_finalizacao(update,setor):
    dados = get_data(setor, context= 'atrasado')
    setor = convert_setor(setor)
    text=f"Produção <b>Em Atraso</b> setor <b>{setor}:</b>{os.linesep}\U00002757{dados['contador']} produtos no setor: <b>{dados['somador']} peças.</b>{os.linesep}"
    for item1,item2 in zip (dados['listaficha'],dados['listadiascostura']):
        text +=f" <b>\U00002714FC: {item1}, {item2} dias na confecção.{os.linesep}</b>"

    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def pedido_track(context: CallbackContext):    
    from roupa.models import Track
    from core.models import User
    track = Track.objects.latest('pcp')
    for index, requisicao in enumerate(track.pcp):
        chat_id = requisicao['user']
        user = User.objects.get(user_bot__user_id = chat_id)
        dadoslacre = requisicao['lacre']
        text=f"\U00002757Acompanhamento do pedido <b>{dadoslacre}:</b>{os.linesep}"
        for produto in get_url():
            if produto['Lacre'] == int(dadoslacre) :
                if produto['Status'] == 1 :
                    text += f"\U0001F3EC Cliente: <b>{produto['Comercial']}</b>{os.linesep}"
                    text += f"\U0000231B Status: <b> Modelagem</b>{os.linesep}"
                    text += f"\U0001F69A Data entrega: <b>{produto['DataEntrega']}</b>"
                elif produto['Status'] == 2 :
                    text += f"\U0001F3EC Cliente: <b>{produto['Comercial']}</b>{os.linesep}"
                    text += f"\U0000231B Status: <b> Encaixe</b>{os.linesep}"
                    text += f"\U0001F69A Data entrega: <b>{produto['DataEntrega']}</b>"
                elif produto['Status'] == 3 :
                    text += f"\U0001F3EC Cliente: <b>{produto['Comercial']}</b>{os.linesep}"
                    text += f"\U0000231B Status: <b> Expedição Tecido</b>{os.linesep}"
                    text += f"\U0001F69A Data entrega: <b>{produto['DataEntrega']}</b>"
                elif produto['Status'] == 4 :
                    text += f"\U00002714 FC: <b>{produto['FichaCorte']}</b>{os.linesep}"
                    text += f"\U0000231B Status: <b> Corte</b>{os.linesep}"
                    text += f"\U0001F3EC Cliente: <b>{produto['Comercial']}</b>{os.linesep}"
                    text += f"\U0001F69A Data entrega: <b>{produto['DataEntrega']}</b>"
                elif produto['Status'] == 5 :
                    text += f"\U00002714 FC: <b>{produto['FichaCorte']}</b>{os.linesep}"
                    text += f"\U0000231B Status: <b> Costura</b>{os.linesep}"
                    text += f"\U0001F3EC Cliente: <b>{produto['Comercial']}</b>{os.linesep}"
                    text += f"\U0001F69A Data entrega: <b>{produto['DataEntrega']}</b>"
                elif produto['Status'] == 6 :
                    text += f"\U00002714 FC: <b>{produto['FichaCorte']}</b>{os.linesep}"
                    text += f"\U0000231B Status: <b> Finalização</b>{os.linesep}"
                    text += f"\U0001F3EC Cliente: <b>{produto['Comercial']}</b>{os.linesep}"
                    text += f"\U0001F69A Data entrega: <b>{produto['DataEntrega']}</b>"
                elif produto['Status'] == 7 :
                    text += f"\U00002714 FC: <b>{produto['FichaCorte']}</b>{os.linesep}"
                    text += f"\U0000231B Status: <b> Lavanderia</b>{os.linesep}"
                    text += f"\U0001F3EC Cliente: <b>{produto['Comercial']}</b>{os.linesep}"
                    text += f"\U0001F69A Data entrega: <b>{produto['DataEntrega']}</b>"
                elif produto['Status'] == 8 :
                    text += f"\U00002714 FC: <b>{produto['FichaCorte']}</b>{os.linesep}"
                    text += f"\U0000231B Status: <b> Qualidade</b>{os.linesep}"
                    text += f"\U0001F3EC Cliente: <b>{produto['Comercial']}</b>{os.linesep}"
                    text += f"\U0001F69A Data entrega: <b>{produto['DataEntrega']}</b>"
                elif produto['Status'] == 9 :
                    text += f"\U00002714 FC: <b>{produto['FichaCorte']}</b>{os.linesep}"
                    text += f"\U0000231B Status: <b> Acabamento</b>{os.linesep}"
                    text += f"\U0001F3EC Cliente: <b>{produto['Comercial']}</b>{os.linesep}"
                    text += f"\U0001F69A Data entrega: <b>{produto['DataEntrega']}</b>"
                elif produto['Status'] == 10 :
                    text += f"\U00002714 FC: <b>{produto['FichaCorte']}</b>{os.linesep}"
                    text += f"\U0000231B Status: <b> Expedição</b>{os.linesep}"
                    text += f"\U0001F3EC Cliente: <b>{produto['Comercial']}</b>{os.linesep}"
                    text += f"\U0001F69A Data entrega: <b>{produto['DataEntrega']}</b>"
                elif produto['Status'] == 11 :
                    text += f"\U00002714 FC: <b>{produto['FichaCorte']}</b>{os.linesep}"
                    text += f"\U0000231B Status: <b> Pronto</b>{os.linesep}"
                    text += f"\U0001F3EC Cliente: <b>{produto['Comercial']}</b>{os.linesep}"
                    text += f"\U0001F69A Data entrega: <b>{produto['DataEntrega']}</b>"
                else :
                    pass

        context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)
        del track.pcp[index]
        track.save()

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
            InlineKeyboardButton("Produtos Parados", callback_data='produtos_parados_lavanderia'),
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]
        
    elif query.data == 'confeccao':
        keyboard = [
        [
            InlineKeyboardButton("Atrasados Oficina", callback_data='atraso_geral_confeccao'),
            InlineKeyboardButton("Produtos por Oficina", callback_data='producao_por_celula'),  

        ],
        [   InlineKeyboardButton("Produtos Finalização", callback_data='produtos_finalizacao'),
            InlineKeyboardButton("Atrasados Finalização", callback_data='atrasados_finalizacao'),
        ],
        [   InlineKeyboardButton("\U0000203C Prazos Estourados", callback_data='prazos_estourados_confeccao'),
        ],
        [   InlineKeyboardButton("\U0000274C Produtos Parados", callback_data='produtos_parados_confeccao'),
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]

    elif query.data == 'expedicao':
        keyboard = [
        [
            InlineKeyboardButton("Entregas Atrasadas", callback_data='atraso_geral_expedicao'),
            InlineKeyboardButton("Produtos Parados", callback_data='produtos_parados_expedicao'),
        ],
        [InlineKeyboardButton("Menu", callback_data='menu')],
        ]

    elif query.data == 'menu':
        keyboard = menu(query, 'nav')

    elif query.data == 'atraso_geral':        
        return producao_em_atraso(query,12)
    
    elif query.data == 'atraso_geral_confeccao':        
        return producao_em_atraso(query,5)    

    elif query.data == 'producao_por_celula':
        return producao_por_celula(query,5)

    elif query.data == 'prazos_estourados_confeccao':
        return prazos_estourados_confeccao(query,5)

    elif query.data == 'produtos_parados_confeccao':
        return producao_parada_costura(query,5)

    elif query.data == 'produtos_finalizacao':
        return produtos_finalizacao(query,6)

    elif query.data == 'atrasados_finalizacao':
        return atrasados_finalizacao(query,6)
    
    elif query.data == 'atraso_geral_lavanderia':        
        return producao_em_atraso(query,7)
    
    elif query.data == 'produtos_parados_lavanderia':
        return producao_parada(query,7)
    
    elif query.data == 'atraso_geral_expedicao':        
        return producao_em_atraso(query,10)

    elif query.data == 'produtos_parados_expedicao':
        return producao_parada(query,10)

    elif query.data == 'parado_geral':        
        return producao_parada(query,12)

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('\U0001F4AC escolha uma opção:', reply_markup=reply_markup, parse_mode=ParseMode.HTML)

def resumo_diario(context: CallbackContext):
    from core.models import UserBot
    users = UserBot.objects.filter(ativo = True)
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
                text += f"""\U00002757<b>{setor}:
                {dados['contador']} </b>lotes: <b>{dados['somador']} peças.</b>{os.linesep}{os.linesep}"""
                        
        try: 
            user_etapa = UserEtapa.objects.get(user = user.id).etapa
            dados = get_data(setor=5,context='atrasado', context2 = user_etapa)
            if dados['contador'] != 0:
                resumo = 1
                setor = "COSTURA"
                text += f"""\U00002757<b>{setor}:
                {dados['contador']}</b>lotes: <b>{dados['somador']} peças.</b> {os.linesep}"""
                for item1,item2,item3 in zip (dados['listaficha'],dados['listadiascostura'],dados['celcostura']):
                    text +=f"<b>FC</b>:{item1},<b>{item2}</b> dias costura<b>({item3})</b>{os.linesep}"
        except:
            pass
            
        if user.lavanderia:
            dados = get_data(7, 'atrasado')
            if dados['contador'] != 0:
                resumo = 1
                setor = "LAVANDERIA"
                text += f"""{os.linesep}\U00002757<b>{setor}:
                {dados['contador']} </b>lotes: <b>{dados['somador']} peças.</b>{os.linesep}"""
                for item in dados['listaficha']:
                    text += f" \U00002714FC: <b>{item}</b>{os.linesep}"

        if user.expedicao:
            dados = get_data(10, 'atrasado')
            if dados['contador'] != 0:
                resumo = 1
                setor = "EXPEDIÇÃO"
                text += f"""{os.linesep}\U00002757<b>{setor}:
                {dados['contador']} </b>lotes: <b>{dados['somador']} peças.</b>{os.linesep}"""
                for item in dados['listaficha']:
                    text += f" \U00002714FC: <b>{item}</b>{os.linesep}"
                
        if resumo == 0:
            text  += f"Tudo certo!!!{os.linesep}"
        
        try:
            context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)

            keyboard = [
                [
                    InlineKeyboardButton("Menu", callback_data='menu'),
                    InlineKeyboardButton("CAMBOS-BI", url='http://scbi.us-west-2.elasticbeanstalk.com/roupa/index'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            text= f"\U0001F4AC Para mais informações:"    
            context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        except:
            pass

def main() -> None:
    from core.models import Bot
    bot = Bot.objects.latest('token')
    token = bot.token      
    updater = Updater(token)    
    updater.dispatcher.add_handler(MessageHandler(Filters.text, menu))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    hora = datetime.time(bot.horas, bot.minutos, 00, 000000) # +3 horas
    up_job = updater.job_queue    
    up_job.run_daily(resumo_diario, time=hora, days=(0, 1, 2, 3, 4, 5))   
    up_job.run_repeating(pedido_track, interval=60.0, first=0) 
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

