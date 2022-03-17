from apscheduler.schedulers.background import BackgroundScheduler
from roupa.views import check_update_api
import bot,botfrota
from pytz import utc

def start():
    scheduler = BackgroundScheduler()                
    scheduler.add_job(bot.iniciar)  
    scheduler.add_job(botfrota.iniciar)
    scheduler.add_job(check_update_api, 'interval', minutes=10)           
    scheduler.start()    