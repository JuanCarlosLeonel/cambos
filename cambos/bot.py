import requests
import time
import json
import os
from roupa.views import get_url
from dateutil import parser
from datetime import datetime


class TelegramBot():
    def __init__(self):
        token = '1852462745:AAF02s1SOqvgZlfxlLX8iFb_uzhgrY5T8cM'
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_mensagens(update_id)
            dados = atualizacao['result']
            if dados:
                for dado in dados:
                    update_id = dado['update_id']                    
                    chat_id = dado["message"]["from"]["id"]    
                    primeira_menssagem = dado['message']['message_id'] == 1
                    resposta = self.criar_resposta(dado, primeira_menssagem)
                    self.responder(resposta, chat_id)
                
    def obter_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)
        
    def criar_resposta(self, mensagem, primeira_mensagem):
        mensagem = mensagem['message']['text']
        if primeira_mensagem == True or mensagem.lower() == 'menu':
            return f'''primeira resposta (menu){os.linesep}1- opçao{os.linesep}2- opçao{os.linesep}'''
        if mensagem == '1':
            return 'resposta 1'
        if mensagem == '2':
            return 'resposta 2'        
        else:
            return f'''opções:{os.linesep}{os.linesep}-> 1{os.linesep}-> 2{os.linesep}-> menu'''
        
    
    def responder(self,resposta,chat_id):
        link_de_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_de_envio)
    

    def send_message():   
        dados = get_url()
        bot_chatID_tony = '1603244057'    
        bot_chatID_joao = '1110999676'    
        token = '1852462745:AAF02s1SOqvgZlfxlLX8iFb_uzhgrY5T8cM'
        total_pecas = 0
        entrega_atraso = 0
        quantidade_atraso = 0
        produto_parado = 0
        for produto in dados:
            decoder = parser.parse(produto['DataEntrega'])
            semana_entrega = datetime.isocalendar(decoder)[1]+1                        
            total_pecas += produto['QuantPecas']
            if produto['Atrasado'] == "Atrasado":
                entrega_atraso += 1
                quantidade_atraso += produto['QuantPecas']
            if produto['Parado'] == "1":
                produto_parado += 1        
        send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={bot_chatID_tony}&parse_mode=Markdown&text=Olá, Tony!'
        requests.get(send_text)
        send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={bot_chatID_tony}&parse_mode=Markdown&text=temos {produto_parado} produtos parados'
        requests.get(send_text)
        send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={bot_chatID_tony}&parse_mode=Markdown&text=e {entrega_atraso} entregas atrasadas.'        
        requests.get(send_text)

        send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={bot_chatID_joao}&parse_mode=Markdown&text=Olá, João Vitor!'
        requests.get(send_text)
        send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={bot_chatID_joao}&parse_mode=Markdown&text=temos {produto_parado} produtos parados'
        requests.get(send_text)
        send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={bot_chatID_joao}&parse_mode=Markdown&text=e {entrega_atraso} entregas atrasadas.'        
        requests.get(send_text)

    

    
