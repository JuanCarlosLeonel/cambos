from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
from bot import TelegramBot
from pytz import utc


bot2 = TelegramBot()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(bot2.Iniciar, 'interval', minutes=1, name='botIniciar')        
    scheduler.add_job(bot2.send_message, 'cron', day_of_week='mon-fri', hour='8', minute='00', name='botRotina', start_date='2021-05-16')        
    scheduler.start()    