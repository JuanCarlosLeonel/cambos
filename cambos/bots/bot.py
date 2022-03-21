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
import datetime

def get_user(update):
    from roupa.models import RoupaBot
    user_id = update.message.chat_id
    userbot = RoupaBot.objects.get(user_id = user_id)
    return userbot

def get_data(setor, context, oficina=None, oficina2 = None):
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
                if not oficina is None:
                    for ofic in oficina:
                        if produto['Celula'] == ofic.nick_spi:
                            if context == 'atrasado':                        
                                if produto['Atrasado'] == "Em Atraso":            
                                    contador += 1
                                    somador += produto['QuantPecas']   
                                    listaficha.append(produto['FichaCorte'])
                                    listadiascostura.append(produto['DiasCostura'])
                                    dataentrega.append(produto['DataEntrega'][8:] + '/' + produto['DataEntrega'][5:7] + '/' + produto['DataEntrega'][0:4])
                                    celcostura.append(produto['Celula'])
                                elif produto['DiasCostura'] >= 18:
                                    contador += 1
                                    somador += produto['QuantPecas']
                                    listaficha.append(produto['FichaCorte'])
                                    listadiascostura.append(produto['DiasCostura'])
                                    dataentrega.append(produto['DataEntrega'][8:] + '/' + produto['DataEntrega'][5:7] + '/' + produto['DataEntrega'][0:4])
                                    celcostura.append(produto['Celula'])
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
                                    listadiascostura.append(produto['DiasCostura'])
                                    dataentrega.append(produto['DataEntrega'][8:] + '/' + produto['DataEntrega'][5:7] + '/' + produto['DataEntrega'][0:4])
                                    celcostura.append(produto['Celula'])
                            elif context == 'parado':
                                if produto['Parado'] == "1":
                                    contador += 1
                                    somador += produto['QuantPecas']
                                    listaficha.append(produto['FichaCorte'])
                                    dataentrega.append(produto['DataEntrega'][8:] + '/' + produto['DataEntrega'][5:7] + '/' + produto['DataEntrega'][0:4])
                                    celcostura.append(produto['Celula'])
                if not oficina2 is None:  #producao por celula
                    if produto['Celula'] == oficina2:
                        if context == 'tudo':
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
                        dataentrega.append(produto['DataEntrega'][8:] + '/' + produto['DataEntrega'][5:7] + '/' + produto['DataEntrega'][0:4]) 
                    elif produto['DiasCostura'] >= 18:
                        contador += 1
                        somador += produto['QuantPecas']
                        listaficha.append(produto['FichaCorte'])
                        dataentrega.append(produto['DataEntrega'][8:] + '/' + produto['DataEntrega'][5:7] + '/' + produto['DataEntrega'][0:4])
                elif context =='pecas':
                    contador +=1
                    somador += produto['QuantPecas']
                    listaficha.append(produto['FichaCorte'])
                    dataentrega.append(produto['DataEntrega'][8:] + '/' + produto['DataEntrega'][5:7] + '/' + produto['DataEntrega'][0:4])                     
        else:
            if produto['Status'] == setor:
                if context == 'atrasado':                        
                    if produto['Atrasado'] == "Em Atraso":            
                        contador += 1
                        somador += produto['QuantPecas']  
                        listaficha.append(produto['FichaCorte'])  
                        dataentrega.append(produto['DataEntrega'][8:] + '/' + produto['DataEntrega'][5:7] + '/' + produto['DataEntrega'][0:4])
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
                        dataentrega.append(produto['DataEntrega'][8:] + '/' + produto['DataEntrega'][5:7] + '/' + produto['DataEntrega'][0:4])
                elif context == 'parado':
                    if produto['Parado'] == "1":
                        contador += 1
                        somador += produto['QuantPecas']
                        listaficha.append(produto['FichaCorte'])
                        dataentrega.append(produto['DataEntrega'][8:] + '/' + produto['DataEntrega'][5:7] + '/' + produto['DataEntrega'][0:4])

    return {'contador':contador,'somador':somador,'listaficha':listaficha,'listadiascostura':listadiascostura,'celcostura':celcostura,'dataentrega':dataentrega}

def return_menu(update, text):
    keyboard = [[InlineKeyboardButton(f'\U000021A9 Menu', callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)    
    update.message.reply_text('\U0001F456', reply_markup=reply_markup)

def producao_em_atraso(update, setor):            
    if setor == 5:
        user = get_user(update)
        c = 0
        text = ""
        celula = user.costura.all()
        dados = get_data(setor, context='atrasado', oficina = celula)            
        if dados['contador'] != 0:
            text = f"""\U00002757Entregas <b>EM ATRASO</b> no setor:
            <b>{dados['contador']}</b> lotes: <b>{dados['somador']}</b> peças. {os.linesep}"""
            for item1,item2,item3 in zip (dados['listaficha'],dados['dataentrega'],dados['celcostura']):
                text +=f"<i>{item1}</i>, <b>Prazo</b>:{item2}<b>,{item3}</b>{os.linesep}"
            if c == 0:
                update.edit_message_text(text, parse_mode=ParseMode.HTML)
                c += 1
            else:
                update.message.reply_text(text, parse_mode=ParseMode.HTML)
    elif setor == 7:
        dados = get_data(setor, context = 'atrasado') 
        setor = convert_setor(setor)           
        text = f"""\U00002757Entregas <b>EM ATRASO</b> no setor:
        <b>{dados['contador']}</b> lotes: <b>{dados['somador']}</b> peças. {os.linesep}"""
        for item1,item2 in zip (dados['listaficha'],dados['dataentrega']):
            text +=f"<b>FC</b>:{item1}, <b>PRAZO: </b>{item2}{os.linesep}"
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
        text = ""
        for oficina in user.costura.all():           
            celula = oficina.nick_spi       
            dados = get_data(setor,context = 'tudo', oficina2 = celula)
            if dados['contador'] != 0:     
                text=f"Produção <b>{celula}:</b>{os.linesep}\U00002757{dados['contador']} entregas: <b>{dados['somador']} peças.</b>{os.linesep}"
                for item1,item2 in zip (dados['listaficha'],dados['listadiascostura']):
                    text +=f"<b>\U00002714FC</b>: {item1}, <b>{item2}</b> dias na costura.{os.linesep}"
                if c == 0:
                    update.edit_message_text(text, parse_mode=ParseMode.HTML)
                    c += 1
                else:
                    update.message.reply_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def prazos_estourados(update, setor):
    if setor == 5:
        user = get_user(update)
        c = 0
        text = "" 
        celula = user.costura.all()
        dados = get_data(setor, context='atrasados', oficina = celula)            
        if dados['contador'] != 0:
            text = f"""\U00002757Entregas com <b>PRAZO ESTOURADO</b> no setor:
            <b>{dados['contador']}</b> lotes: <b>{dados['somador']} peças.</b> {os.linesep}"""
            for item1,item2,item3 in zip (dados['listaficha'],dados['dataentrega'],dados['celcostura']):
                text +=f"<b>FC</b>{item1},<b>Prazo</b>{item2}<b>,{item3}</b>{os.linesep}"
            if c == 0:
                update.edit_message_text(text, parse_mode=ParseMode.HTML)
                c += 1
            else:
                update.message.reply_text(text, parse_mode=ParseMode.HTML)
    elif setor == 7:
        dados = get_data(setor, context = 'atrasados')
        setor = convert_setor(setor)
        text = f"""\U00002757Entregas com <b>PRAZO ESTOURADO</b> no setor:
        <b>{dados['contador']}</b> lotes: <b>{dados['somador']} peças.</b>{os.linesep}"""
        for item1,item2 in zip (dados['listaficha'],dados['dataentrega']):
            text +=f"<b>FC</b>:{item1}, <b>PRAZO: </b>{item2}{os.linesep}"
        update.edit_message_text(text, parse_mode=ParseMode.HTML)
    elif setor == 10:
        dados = get_data(setor, context = 'atrasados')
        setor = convert_setor(setor)
        text = f"""\U00002757Entregas com <b>PRAZO ESTOURADO</b> no setor:
        <b>{dados['contador']}</b> lotes: <b>{dados['somador']} peças.</b>{os.linesep}"""
        for item1,item2 in zip (dados['listaficha'],dados['dataentrega']):
            text +=f"<b>FC</b>:{item1}, <b>PRAZO: </b>{item2}{os.linesep}"
        update.edit_message_text(text, parse_mode=ParseMode.HTML)

    return return_menu(update, text)

def producao_parada(update, setor):
    dados = get_data(setor, context = 'parado')
    setor = convert_setor(setor)
    text=f"Produção <b>{setor}:</b> {os.linesep}\U00002757 {dados['contador']} produtos PARADOS: <b>{dados['somador']} peças.</b>{os.linesep}"
    for item in dados['listaficha']:
        text +=f"<b>\U00002714FC: {item}</b>{os.linesep}"
    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def producao_parada_costuralavanexp(update, setor):
    if setor == 5:
        user = get_user(update)
        c = 0
        text = ""
        celula = user.costura.all()
        dados = get_data(setor, context='parado', oficina = celula)            
        if dados['contador'] != 0:
            text = f"""\U00002757Entregas <b>PARADAS</b> no setor:
            <b>{dados['contador']}</b> lotes: <b>{dados['somador']} peças.</b> {os.linesep}"""
            for item1,item2,item3 in zip (dados['listaficha'],dados['dataentrega'],dados['celcostura']):
                text +=f"<b>FC</b>{item1},<b>Prazo</b>{item2}<b>,{item3}</b>{os.linesep}"
            if c == 0:
                update.edit_message_text(text, parse_mode=ParseMode.HTML)
                c += 1
            else:
                update.message.reply_text(text, parse_mode=ParseMode.HTML)
    elif setor == 7:
        dados = get_data(setor, context = 'parado')
        setor = convert_setor(setor)
        text = f"""\U00002757Entregas <b>PARADAS</b> no setor:
        <b>{dados['contador']}</b> lotes: <b>{dados['somador']} peças.</b>{os.linesep}"""
        for item1,item2 in zip (dados['listaficha'],dados['dataentrega']):
            text +=f"<b>FC</b>:{item1}, <b>PRAZO: </b>{item2}{os.linesep}"
        update.edit_message_text(text, parse_mode=ParseMode.HTML)
    elif setor == 10:
        dados = get_data(setor, context = 'parado')
        setor = convert_setor(setor)
        text = f"""\U00002757Entregas <b>PARADAS</b> no setor:
        <b>{dados['contador']}</b> lotes: <b>{dados['somador']} peças.</b>{os.linesep}"""
        for item1,item2 in zip (dados['listaficha'],dados['dataentrega']):
            text +=f"<b>FC</b>:{item1}, <b>PRAZO: </b>{item2}{os.linesep}"
        update.edit_message_text(text, parse_mode=ParseMode.HTML)
    
    return return_menu(update, text)

def produtos_finalizacao(update, setor): 
    dados = get_data(setor, context= 'pecas')
    setor = convert_setor(setor)
    text=f"Produção <b>{setor}:</b>{os.linesep}\U00002757{dados['contador']} produtos no setor: <b>{dados['somador']} peças.</b>{os.linesep}"
    for item1,item2 in zip (dados['listaficha'],dados['dataentrega']):
        text +=f"<b>FC</b>:{item1}, <b>PRAZO: </b>{item2}{os.linesep}"

    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def atrasados_finalizacao(update,setor):
    dados = get_data(setor, context= 'atrasado')
    setor = convert_setor(setor)
    text=f"Produção <b>Em Atraso</b> setor <b>{setor}:</b>{os.linesep}\U00002757{dados['contador']} produtos no setor: <b>{dados['somador']} peças.</b>{os.linesep}"
    for item1,item2 in zip (dados['listaficha'],dados['dataentrega']):
        text +=f"<b>FC</b>:{item1}, <b>PRAZO: </b>{item2}{os.linesep}"

    update.edit_message_text(text, parse_mode=ParseMode.HTML)
    return return_menu(update, text)

def pedido_track(context: CallbackContext):    
    from roupa.models import Track    
    track = Track.objects.latest('pcp')
    for index, requisicao in enumerate(track.pcp):
        chat_id = requisicao['user']        
        dadoslacre = requisicao['lacre']
        for produto in get_url():
            produto["Status"] = convert_setor(produto["Status"])
            if produto['Lacre'] == int(dadoslacre) :
                text=f"\U00002757Acompanhamento do código <b>{produto['Modelo']}:</b>{os.linesep}"
                text += f"\U000023F3 Status: <b>{produto['Status']}</b>{os.linesep}"
                if produto['FichaCorte'] != None:
                    text += f"\U00002714 FC: <b>{produto['FichaCorte']}</b>{os.linesep}"
                text += f"\U0001F3EC Cliente: <b>{produto['Nome']}</b>{os.linesep}"
                text += f"\U0001F69A Data entrega: <b>{produto['DataEntrega'][8:] + '/' + produto['DataEntrega'][5:7] + '/' + produto['DataEntrega'][0:4]}</b>"
            else :
                pass
        context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)
        keyboard = [
            [
                InlineKeyboardButton("Menu", callback_data='menu'),
                InlineKeyboardButton("CAMBOS-BI", url='https://indicador.souzacambos.com.br/'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text= f"\U0001F4AC Para mais informações:"    
        context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        del track.pcp[index]
        track.save()

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
    mensagem = update.message.text  
    try:
        userbot = get_user(update)
        text = f"\U0001F4AC Escolha uma opção:"
        dict = {}  
        if userbot.geral:
             dict['Geral']='geral'

        if userbot.costura.count() > 0:
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
        p = RoupaBot(user_id = chat_id, user_nome = first_name)
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
            InlineKeyboardButton("Atrasados Lavanderia", callback_data='atraso_geral_lavanderia'),
            InlineKeyboardButton("\U0000274C Produtos Parados", callback_data='produtos_parados_lavanderia'),
        ],
        [   InlineKeyboardButton("\U0000203C Prazos Estourados", callback_data='prazos_estourados_lavanderia'),
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
            InlineKeyboardButton("Atrasados Expedição", callback_data='atraso_geral_expedicao'),
            InlineKeyboardButton("\U0000274C Produtos Parados", callback_data='produtos_parados_expedicao'),
        ],
        [   InlineKeyboardButton("\U0000203C Prazos Estourados", callback_data='prazos_estourados_expedicao'),
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
        return prazos_estourados(query,5)

    elif query.data == 'produtos_parados_confeccao':
        return producao_parada_costuralavanexp(query,5)

    elif query.data == 'produtos_finalizacao':
        return produtos_finalizacao(query,6)

    elif query.data == 'atrasados_finalizacao':
        return atrasados_finalizacao(query,6)
    
    elif query.data == 'atraso_geral_lavanderia':        
        return producao_em_atraso(query,7)

    elif query.data == 'prazos_estourados_lavanderia':        
        return prazos_estourados(query,7)
    
    elif query.data == 'produtos_parados_lavanderia':
        return producao_parada_costuralavanexp(query,7)
    
    elif query.data == 'atraso_geral_expedicao':        
        return producao_em_atraso(query,10)

    elif query.data == 'prazos_estourados_expedicao':        
        return prazos_estourados(query,10)

    elif query.data == 'produtos_parados_expedicao':
        return producao_parada_costuralavanexp(query,10)

    elif query.data == 'parado_geral':        
        return producao_parada(query,12)

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('\U0001F4AC Escolha uma opção:', reply_markup=reply_markup, parse_mode=ParseMode.HTML)

def resumo_diario(context: CallbackContext):
    from roupa.models import RoupaBot
    users = RoupaBot.objects.filter(ativo = True)
    for user in users:        
        resumo = 0
        chat_id = user.user_id
        text=f"""\U00002709 Bom dia, {user.user_nome}! {os.linesep}
        Segue relatório de produção em atraso:{os.linesep}{os.linesep}"""
                 
        if user.geral:
            dados = get_data(12, 'atrasado')
            if dados['contador'] != 0:
                resumo = 1
                text += f"""\U00002757<b>GERAL:
                {dados['contador']} </b>lotes: <b>{dados['somador']} peças.</b>{os.linesep}{os.linesep}"""
                        
        try: 
            celula = user.costura.all()
            dados = get_data(setor=5,context='atrasado', oficina = celula)            
            if dados['contador'] != 0:
                resumo = 1
                text += f"""\U00002757<b>COSTURA:
                {dados['contador']} </b>lotes: <b>{dados['somador']} peças.</b>{os.linesep}"""
                for item1,item2,item3 in zip (dados['listaficha'],dados['dataentrega'],dados['celcostura']):
                    text +=f"<i>{item1}</i>, <b>Prazo</b>:{item2}<b>,{item3}</b>{os.linesep}"
        except:
            text += "erro costura"
            
        if user.lavanderia:
            dados = get_data(7, 'atrasado')
            if dados['contador'] != 0:
                resumo = 1
                text += f"""{os.linesep}\U00002757<b>LAVANDERIA:
                {dados['contador']}</b> lotes: <b>{dados['somador']} peças.</b>{os.linesep}"""
                for item1,item2 in zip (dados['listaficha'],dados['dataentrega']):
                    text += f"<i>{item1}</i>, <b>Prazo: </b>{item2}{os.linesep}"

        if user.expedicao:
            dados = get_data(10, 'atrasado')
            if dados['contador'] != 0:
                resumo = 1
                text += f"""{os.linesep}\U00002757<b>EXPEDIÇÃO:
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
                    InlineKeyboardButton("CAMBOS-BI", url='https://indicador.souzacambos.com.br/'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            text= f"\U0001F4AC Para mais informações:"    
            context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        except:
            pass


def pesquisa_corte(update, context):
    chat_id = update.message.chat_id
    mensagem = update.message.text
    for produto in get_url():
        produto["Status"] = convert_setor(produto["Status"])
        if produto['FichaCorte'] == mensagem or str(produto['Modelo']) == mensagem or str(produto['Lacre']) == mensagem or produto['Atrasado'] == mensagem:
            text = f"\U00002714<b>Detalhes do Pedido:</b>{os.linesep}"
            if produto['FichaCorte'] != None:
                text += f"\U000027a1 FC: <b>{produto['FichaCorte']}</b>{os.linesep}"
            else:
                text += f"\U000027a1 FC: <b>Em elaboração.</b>{os.linesep}"
            text += f"\U0001F522 QuantPeças: <b>{produto['QuantPecas']}</b>{os.linesep}"
            text += f"\U0001F4CB Código: <b>{produto['Modelo']}</b>{os.linesep}"
            if produto['ValorDentro'] != None:
                text += f"\U00002712 Valor: <b>{produto['ValorDentro']}</b>{os.linesep}"
            else:
                text += f"\U00002712 Valor: <b>Em definição</b>{os.linesep}"
            text += f"\U0001F3EC Cliente: <b>{produto['Nome']}</b>{os.linesep}"
            if produto['Celula'] != None:
                text += f"\U00002702 Célula Costura: <b>{produto['Celula']}</b>{os.linesep}"
            else:
                text += f"\U00002702 Cél Costura:<b> Não definida.</b>{os.linesep}"
            if produto['DiasCostura'] != None:
                text += f"\U0001F5D3 Dias na Costura: <b>{produto['DiasCostura']} dias</b>{os.linesep}"
            else:
                text += f"\U0001F5D3 Dias na Costura: <b> 0 dias</b>{os.linesep}"
            text += f"\U000023F0 Prazo Restante: <b>{produto['Diasresto']} dias</b>{os.linesep}"
            text += f"\U000023F3 Status: <b>{produto['Status']}</b>{os.linesep}"
            text += f"\U0000203C Situação: <b>{produto['Atrasado'].upper()}</b>{os.linesep}"
            text += f"\U0001F69A Data entrega: <b>{produto['DataEntrega'][8:] + '/' + produto['DataEntrega'][5:7] + '/' + produto['DataEntrega'][0:4]}</b>{os.linesep}"
            context.bot.send_chat_action(chat_id, "typing")
            update.message.reply_text(text, parse_mode=ParseMode.HTML)
        else:
            pass
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
    bot = Bot.objects.get(nome = 'PCP')
    token = bot.token      
    updater = Updater(token)  
    # updater.dispatcher.add_handler(MessageHandler(Filters.text, menu))  
    updater.dispatcher.add_handler(MessageHandler(Filters.text, pesquisa_corte))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    hora = datetime.time(bot.horas, bot.minutos, 00, 000000) # +3 horas
    up_job = updater.job_queue    
    up_job.run_daily(resumo_diario, time=hora, days=(0, 1, 2, 3, 4, 5)) 
    # up_job.run_daily(entrada_costura, datetime.time(hour=12, minute=35), days=(0, 1, 2, 3, 4, 5))  
    up_job.run_repeating(pedido_track, interval=60.0, first=0) 
    #up_job.run_once(resumo_diario, 10)
    updater.start_polling()
    updater.idle()

def iniciar():
    from core.models import Bot
    ativo= Bot.objects.get(nome = 'PCP').ativo            
    if ativo:
        return main()   

      
if __name__ == '__main__':
    main()