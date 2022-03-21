from django.db import models
from jsonfield import JSONField
from django_currentuser.db.models import CurrentUserField
from core.models import Pessoa, Setor, User
from roupa.models import Etapa, Processo
import datetime

class Auditor(models.Model):    
    auditor_interno = models.ForeignKey(Pessoa, null=True, blank=True, on_delete=models.DO_NOTHING, db_constraint=False)
    auditor_externo = models.CharField(max_length=20, null=True, blank=True)        
    oficina         = models.ForeignKey(Etapa, null=True, blank=True, on_delete=models.SET_NULL)
    data_criacao  = models.DateField(verbose_name="Data", default=datetime.date.today)
    created_by    = CurrentUserField()

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
    data_criacao  = models.DateField(verbose_name="Data", default=datetime.date.today)
    created_by    = CurrentUserField()

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
    data_criacao  = models.DateField(verbose_name="Data", default=datetime.date.today)
    created_by    = CurrentUserField()


    def __str__(self):
        return f'{self.descricao} - {self.volume}'
    
    class Meta:        
        db_table = 'qualidade"."inspecao'


class PlanoDeAcao(models.Model):
    TIPOACAO = (
            ('Disposição', 'Disposição'),
            ('Corretiva', 'Corretiva'),                                     
            ('Preventiva', 'Preventiva'),                                     
        )
    ORIGEMACAO = (
            ('Não Conformidade', 'Não Conformidade'),
            ('Melhoria', 'Melhoria'),                                     
            ('Pesquisa', 'Pesquisa'),                                     
        )
    TIPOREF = (
            ('Ficha de Produção', 'Ficha de Produção'),            
        )    
    
    tipo_acao       = models.CharField(max_length=10, choices=TIPOACAO, default='Disposição')
    origem_acao     = models.CharField(max_length=16, choices=ORIGEMACAO, default='Não Conformidade')
    tipo_referencia = models.CharField(max_length=17, choices=TIPOREF, default='Ficha de Produção')
    referencia      = models.CharField(max_length=20)    
    data_fim        = models.DateField(verbose_name="fim", blank=True, null=True)
    eficaz          = models.BooleanField(blank=True, null=True)
    evidencia       = models.CharField(max_length=20, null=True, blank=True)
    created_by      = CurrentUserField()
    data_criacao    = models.DateField(verbose_name="Data", default=datetime.date.today)
    
    def __str__(self):
        return f'{self.referencia} - {self.tipo_acao}'
    
    class Meta:        
        db_table = 'qualidade"."PlanoDeAcao'


class Acao(models.Model):
    
    plano_acao    = models.ForeignKey(PlanoDeAcao, on_delete=models.CASCADE)    
    descricao     = models.CharField(max_length=100)    
    responsavel   = models.ForeignKey(User, related_name="AcaoResponsavel", on_delete=models.SET_NULL, null=True)    
    data_prazo    = models.DateField(verbose_name="Prazo")
    data_inicio   = models.DateField(verbose_name="inicio", null=True, blank=True)
    data_fim      = models.DateField(verbose_name="fim", null=True, blank=True)
    resposta      = models.CharField(max_length=100, null=True, blank=True)    
    data_criacao  = models.DateField(verbose_name="Data", default=datetime.date.today)
    created_by    = CurrentUserField()
    
    def __str__(self):
        return f'{self.referencia} - {self.tipo_acao}'
    
    class Meta:        
        db_table = 'qualidade"."Acao'


class QualidadeBot(models.Model):    
    user_id       = models.BigIntegerField(unique=True)
    user_nome     = models.CharField(max_length=30)    
    pedido_parado = models.BooleanField(default=False)
    ver_acoes     = models.BooleanField(default=False)
    ativo         = models.BooleanField(default=True)
    usuario       = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.user_nome}'


class QualidadeTrack(models.Model):    
    pcp = JSONField()
