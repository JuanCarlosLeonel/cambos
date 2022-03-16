from django.db import models
from jsonfield import JSONField
from django_currentuser.db.models import CurrentUserField
from core.models import Pessoa, Setor
from roupa.models import Etapa, Processo

# tabela para apagar após migração do BD.
class FichaCorte(models.Model):    
    lacre       = models.IntegerField()        
    ficha_corte = models.CharField(max_length=7, null=True, blank=True)        
    dados       = models.JSONField()
    def __str__(self):
        return f'{self.ficha_corte}'
    
    class Meta:        
        db_table = 'qualidade"."FichaCorte'


class Auditor(models.Model):    
    auditor_interno = models.ForeignKey(Pessoa, null=True, blank=True, on_delete=models.DO_NOTHING, db_constraint=False)
    auditor_externo = models.CharField(max_length=20, null=True, blank=True)        
    oficina         = models.ForeignKey(Etapa, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.auditor_interno}{self.auditor_externo} / {self.oficina}'
    
    class Meta:        
        db_table = 'qualidade"."auditor'


class TabelaAmostragem(models.Model):    
    descricao         = models.CharField(max_length=20)        
    
    def __str__(self):
        return f'{self.descricao}'
    
    class Meta:        
        db_table = 'qualidade"."tabelaamostragem'

class ItemTabelaAmostragem(models.Model):    
    tabela_amostragem  = models.ForeignKey(TabelaAmostragem, on_delete=models.CASCADE)
    quantidade_minima = models.IntegerField()
    quantidade_maxima = models.IntegerField()
    amostragem        = models.IntegerField()

    def __str__(self):
        return f'{self.tabela_amostragem}:  {self.quantidade_minima} ~ {self.quantidade_maxima}: {self.amostragem} '
    
    class Meta:        
        db_table = 'qualidade"."itemtabelaamostragem'


class Inspecao(models.Model):
    VOLUMEINSPECAO = (
            ('Total', 'Total'),
            ('Percentual', 'Percentual'),                                     
            ('Tabela', 'Tabela'),                                     
        )
    descricao             = models.CharField(max_length=20)
    setor                 = models.ForeignKey(Processo, on_delete=models.CASCADE)
    volume                = models.CharField(max_length=10, choices=VOLUMEINSPECAO, default='Percentual')
    tabela                = models.ForeignKey(TabelaAmostragem, on_delete=models.SET_NULL, null=True, blank=True)
    percentual_amostragem = models.IntegerField()
    criterio_aprovacao    = models.IntegerField()


    def __str__(self):
        return f'{self.descricao} - {self.volume}'
    
    class Meta:        
        db_table = 'qualidade"."inspecao'
