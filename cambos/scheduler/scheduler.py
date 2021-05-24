from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
import bot
from bot2 import TelegramBot
from pytz import utc

bot3 = TelegramBot()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(bot.main, 'cron', day_of_week='mon', hour='20', minute='18', name='botIniciar')        
    scheduler.add_job(bot3.send_message, 'cron', day_of_week='mon-fri', hour='19', minute='59', name='botRotina', start_date='2021-05-16')        
    scheduler.start()    