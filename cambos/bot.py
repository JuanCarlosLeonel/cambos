import requests
import time
import json

class telegrambot():
    def __init__(self):
        token = '1852462745:AAF02s1SOqvgZlfxlLX8iFb_uzhgrY5T8cM'
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def send_message():        
        bot_chatID_tony = '1603244057'        
        token = '1852462745:AAF02s1SOqvgZlfxlLX8iFb_uzhgrY5T8cM'
        n=0
        while n < 1:
            send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id=' + bot_chatID_tony + '&parse_mode=Markdown&text=' + "Tony4"
            n += 1
            time.sleep(10)
            requests.get(send_text)


    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_novas_mensagens(update_id)
            dados = atualizacao["result"]
            if dados:
                for dado in dados:
                    update_id = dado['update_id']
                    mensagem = str(dado["message"]["text"])
                    chat_id = dado["message"]["from"]["id"]
                    eh_primeira_mensagem = int(
                        dado["message"]["message_id"]) == 1
                    resposta = self.criar_resposta(
                        mensagem, eh_primeira_mensagem)
                    self.responder(resposta, chat_id)

    # Obter mensagens
    def obter_novas_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)
