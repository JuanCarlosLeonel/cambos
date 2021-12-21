from django.db import models
from core.models import Pessoa

class Motorista(models.Model):
    nome    = models.ForeignKey(Pessoa, null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    cnh     = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.nome}'
    
    class Meta:        
        db_table = 'frota"."motorista' 