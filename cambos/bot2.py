import requests
import time
import json
import os
from roupa.views import get_url
from dateutil import parser
from datetime import date, datetime, timedelta
from core.models import Bot, UserBot
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class TelegramBot():
    def __init__(self):
        self.bot = Bot.objects.latest('token')
        token = self.bot.token
        self.bot = telegram.Bot(token=token)
        self.url_base = f'https://api.telegram.org/bot{token}/'
        self.dados = get_url()


    def Iniciar(self):
        update_id = None
        while True:
            ativo= Bot.objects.latest('token').ativo            
            if ativo:
                atualizacao = self.obter_mensagens(update_id)
                if atualizacao['result']:
                    dados = atualizacao['result']                
                                         
                    for dado in dados:
                        try:
                            update_id = dado['update_id']
                            try:                    
                                chat_id = dado["message"]["from"]["id"]    
                            except:
                                chat_id = dado['callback_query']["message"]["from"]["id"]    
                            resposta = self.criar_resposta(dado)
                            self.responder(resposta, chat_id)
                        except:
                            pass
                    time.sleep(20)
                else:
                    break
            else:
                break
                    
    def obter_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=200'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)
        
    def criar_resposta(self, dado):
        from core.models import UserBot
        try:
            user = dado["message"]["from"]["first_name"]
            user_id = dado["message"]["from"]["id"]
            mensagem = dado['message']['text']
        except:
            user = dado['callback_query']["message"]["from"]["first_name"]
            user_id = dado['callback_query']["message"]["from"]["id"]
            mensagem = dado['callback_query']['message']['text']
       
        try:
            userbot = UserBot.objects.get(user_id = user_id)
        except:
            p = UserBot(user_id = user_id, user_nome = user)
            p.save() 
            text = f'Olá {user}!{os.linesep}Obrigado por acessar nosso sistema.{os.linesep}Já já seu acesso será liberado.'   
            return {'text':text, 'dict':{}}
        try:
            data = dado['callback_query']['data']
        except:
            data = False        
                    
        if data:
            
            text = f'{data},tercerizado.'   
            return {'text':text, 'dict':{}}   
        elif mensagem == '1':     
            text = f'{data},terc.'   
            return {'text':text, 'dict':{}}   
        else:            
            return self.menu(userbot)                    
            
    def menu(self, userbot):        
        menu = f'escolha uma opção:{os.linesep}{os.linesep}'
        dict = {}        
        if userbot.oficina.count() > 0:
            dict['Terceirizados']='terceirizados'
        if userbot.lavanderia:
            dict['Lavanderia']='lavanderia'
        return {'text':menu, 'dict':dict}
    
    def terceirizado(self, user_id, user):
        user_bot = UserBot.objects.get(user_id=user_id)
        menu = f'olá, {user}!:{os.linesep}escolha uma opção:{os.linesep}{os.linesep}'
        dict = {}
        
        if user_bot.oficina.count() > 0:
            dict['oficina1']='terceirizados'
        if user_bot.lavanderia:
            dict['Oficina2']='lavanderia'
        return {'text':menu, 'dict':dict}

    def send_message(self):             
        total_pecas = 0
        entrega_atraso = 0
        quantidade_atraso = 0
        produto_parado = 0        
        for produto in self.dados:
            data = parser.parse(produto['DataEntrega'])            
            total_pecas += produto['QuantPecas']
            if produto['Atrasado'] == "Atrasado":
                entrega_atraso += 1
                quantidade_atraso += produto['QuantPecas']
            if produto['Parado'] == "1":
                produto_parado += 1  
               
        for user in UserBot.objects.all():
            resposta = f'Oi {user.user_nome}!'
            self.responder(resposta, user.user_id)
            if user.geral==True:
                resposta = f"No Geral, temos {produto_parado} produtos parados {os.linesep}e {entrega_atraso} entregas atrasadas."
                self.responder(resposta, user.user_id)
            if user.oficina.count() > 0:                
                resposta = f'Em Atraso - Oficinas:{os.linesep}{os.linesep}'                 
                for oficina in user.oficina.all():                
                    count = 0
                    soma = 0
                    for produto in self.dados:
                        if produto['Status'] == 5:
                            if produto['Celula'] == oficina.choice:
                                if produto['DiasCostura'] >= 15:
                                    count += 1                    
                                    soma += produto['QuantPecas']
                    if count > 0:       
                        resposta = f'{oficina.choice}:{os.linesep}'                 
                        resposta += f"{count} lotes / {soma} peças"
                        self.responder(resposta, user.user_id)
            if user.lavanderia==True:
                resposta = f'Em Atraso - Lavanderia: {os.linesep}{os.linesep}'
                count = 0
                soma = 0
                for produto in self.dados:
                    if produto['Status'] == 7:
                        if produto['DiasLavanderia'] >= 5:
                            count += 1                    
                            soma += produto['QuantPecas']
                if count == 0:
                    resposta += "Nenhum produto em atraso."
                else:
                    resposta += f"{count} lotes / {soma} peças"
                self.responder(resposta, user.user_id)
            

    def responder(self,resposta,chat_id):   
        self.bot.sendMessage(chat_id,text = resposta)