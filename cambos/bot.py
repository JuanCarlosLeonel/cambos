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
                            primeira_menssagem = dado['message']['message_id'] == 1
                            resposta = self.criar_resposta(dado, primeira_menssagem)
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
        
    def criar_resposta(self, mensagem, primeira_mensagem):
        from core.models import UserBot
        user = mensagem["message"]["from"]["first_name"]
        user_id = mensagem["message"]["from"]["id"]
        mensagem = mensagem['message']['text']
        try:
            userbot = UserBot.objects.get(user_id = user_id)
        except:
            userbot = False
        if not userbot:
            p = UserBot(user_id = user_id, user_nome = user)
            p.save()        
            return f'Olá {user}!{os.linesep}Obrigado por acessar nosso sistema.{os.linesep}Já já seu acesso será liberado.'        
        else:
            if primeira_mensagem == True or mensagem.lower() == 'menu':
                return f'''olá, {user}!:{os.linesep}escolha uma opção:{os.linesep}{os.linesep} 1 -->  Relação de Entregas{os.linesep} 2 --> Agendamento de Entregas das oficinas (vem aí)'''
            if mensagem == '1':                
                relacao = f'Lavanderia: {os.linesep}{os.linesep}'                
                for item in self.dados:
                    if item['Status'] == 7:
                        if item['DiasLavanderia'] >= 5:
                            relacao += f".{item['FichaCorte']} - {item['Modelo']} {os.linesep}"
                return relacao
            if mensagem == '2':
                return 'Em breve'        
            else:
                return f'''escolha uma opção, {user}:{os.linesep}{os.linesep} 1 -->  Atraso Lavanderia{os.linesep} 2 --> Agendamento das oficinas (vem aí)'''    
            
    
    def send_message(self):           
        bot_chatID_tony = '1603244057'    
        bot_chatID_joao = '1110999676'    
        total_pecas = 0
        entrega_atraso = 0
        quantidade_atraso = 0
        produto_parado = 0        
        for produto in self.dados:
            semana = parser.parse(produto['DataEntrega'])            
            total_pecas += produto['QuantPecas']
            if produto['Atrasado'] == "Atrasado":
                entrega_atraso += 1
                quantidade_atraso += produto['QuantPecas']
            if produto['Parado'] == "1":
                produto_parado += 1  
               
        for user in UserBot.objects.all():
            resposta = f'b=Bom dia, {user.user_nome}!'
            self.responder(resposta, user.user_id)
            if user.lavanderia==True:
                resposta += f'Em Atraso - Lavanderia: {os.linesep}{os.linesep}'
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
            if user.geral==True:
                resposta = f"No Geral, temos {produto_parado} produtos parados {os.linesep}e {entrega_atraso} entregas atrasadas."
                self.responder(resposta, user.user_id)
        

    def responder(self,resposta,chat_id):
        link_de_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_de_envio)