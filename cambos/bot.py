import requests
import time
import json
import os
from roupa.views import get_url
from dateutil import parser
from datetime import date, datetime, timedelta
from core.models import Bot, UserBot


class TelegramBot():
    def __init__(self):
        self.bot = Bot.objects.latest('token')
        token = self.bot.token
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
                            chat_id = dado["message"]["from"]["id"]    
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
        user = dado["message"]["from"]["first_name"]
        user_id = dado["message"]["from"]["id"]
        mensagem = dado['message']['text']
        try:
            userbot = UserBot.objects.get(user_id = user_id)
        except:
            userbot = False
        if not userbot:
            p = UserBot(user_id = user_id, user_nome = user)
            p.save()        
            return f'Olá {user}!{os.linesep}Obrigado por acessar nosso sistema.{os.linesep}Já já seu acesso será liberado.'        
        else:            
            return self.menu(user_id, user)            

            
    def menu(self, user_id, user):
        user_bot = UserBot.objects.get(user_id=user_id)
        menu = f'olá, {user}!:{os.linesep}escolha uma opção:{os.linesep}{os.linesep}'
        if user_bot.oficina.count() > 0:
            menu += f' 1 --> Em breve{os.linesep}'
        if user_bot.lavanderia:
            menu += f' 2 --> Em breve{os.linesep}'        
        return menu
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
            resposta = f'Bom dia, {user.user_nome}!'
            self.responder(resposta, user.user_id)
            if user.geral==True:
                resposta = f"No Geral, temos {produto_parado} produtos parados {os.linesep}e {entrega_atraso} entregas atrasadas."
                self.responder(resposta, user.user_id)
            if user.oficina.count() > 0:                
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
                        resposta = f'Em Atraso - Oficinas:{os.linesep}{os.linesep} {oficina.choice}:{os.linesep}'                 
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
        link_de_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_de_envio)