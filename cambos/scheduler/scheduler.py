from apscheduler.schedulers.background import BackgroundScheduler
from roupa.views import check_update_api
import bot
#from bot2 import TelegramBot
from pytz import utc

#bot3 = TelegramBot()

def start():
    scheduler = BackgroundScheduler()                
    scheduler.add_job(bot.iniciar)  
    scheduler.add_job(check_update_api, 'interval', minutes=5)       
    #scheduler.add_job(bot3.send_message, 'cron', day_of_week='mon-fri', hour='8', minute='00', name='botRotina', start_date='2021-05-16')        
    scheduler.start()    