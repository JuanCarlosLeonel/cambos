from django.core.management.base import BaseCommand
from datetime import date
import time
import requests


class Command(BaseCommand):
    
    def handle(self, *args, **options):

        bot_token = '1852462745:AAF02s1SOqvgZlfxlLX8iFb_uzhgrY5T8cM'
        bot_chatID = '1603244057'
        n=0
        while n < 2:
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + "teste56"
            n += 1
            time.sleep(10)
            requests.get(send_text)

        
                