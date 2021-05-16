from django.apps import AppConfig
import os


class CoreConfig(AppConfig):
    name = 'core'
    def ready(self):
        from scheduler import scheduler        
        scheduler.start()
