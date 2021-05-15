from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
from bot import TelegramBot

# This is the function you want to schedule - add as many as you want and then register them in the start() function below

bot2 = TelegramBot()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(bot2.Iniciar, 'interval', minutes=1, name='botIniciar')        
    #scheduler.add_job(TelegramBot.send_message, 'interval', seconds=10, name='botRotina')        
    scheduler.start()    