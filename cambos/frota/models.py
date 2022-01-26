from django.db import models
from core.models import Pessoa, Ativo, User
from django_currentuser.db.models import CurrentUserField
import datetime


class Veiculo(models.Model):
    descricao   = models.ForeignKey(Ativo, null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    placa       = models.CharField(max_length=20, null=True, blank=True)    
    caminhao    = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.descricao}'
    
    class Meta:        
        db_table = 'frota"."veiculo'


class Viagem(models.Model):
    veiculo      = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING, blank=True)
    motorista    = models.ForeignKey(Pessoa, on_delete=models.DO_NOTHING, db_constraint=False)
    data_inicial = models.DateField(blank=True, null=True)
    data_final   = models.DateField(blank=True, null=True)
    hora_inicial = models.TimeField(blank=True, null=True)
    hora_final   = models.TimeField(blank=True, null=True)
    origem       = models.CharField(max_length=40, blank=True)
    destino      = models.CharField(max_length=40)
    carga        = models.CharField(max_length=40, blank=True)
    peso         = models.FloatField(blank=True, null=True)
    km_inicial   = models.IntegerField(blank=True, null=True)
    km_final     = models.IntegerField(blank=True, null=True)
    created_by   = CurrentUserField()
    data_criacao = models.DateField(verbose_name="Data", default=datetime.date.today)

    def __str__(self):
        return f'{self.origem} - {self.destino}'
    
    class Meta:        
        db_table = 'frota"."viagem'
        ordering = ["-data_criacao"]


class Abastecimento(models.Model):
    COMBUSTIVEL = (
            ('Diesel', 'Diesel'),
            ('Gasolina', 'Gasolina'),             
            ('Álcool', 'Álcool'),                         
        )
    veiculo        = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING, blank=True)
    combustivel = models.CharField(max_length=40, choices=COMBUSTIVEL)
    data           = models.DateField()        
    valor_unitario = models.FloatField()
    quantidade     = models.FloatField()

    def __str__(self):
        return f'{self.veiculo}'
    
    class Meta:        
        db_table = 'frota"."abastecimento'


class Infracao(models.Model):    
    veiculo    = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING)
    data       = models.DateField()    
    valor      = models.FloatField()
    motivo     = models.CharField(max_length=40)
    
    def __str__(self):
        return f'{self.veiculo} - {self.valor}'
    
    class Meta:        
        db_table = 'frota"."infracao'


class Seguro(models.Model):    
    veiculo    = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING)
    data       = models.DateField()    
    valor      = models.FloatField()
    descricao  = models.CharField(max_length=40)
    
    def __str__(self):
        return f'{self.veiculo} - {self.valor}'
    
    class Meta:        
        db_table = 'frota"."seguro'


class Rastreio(models.Model):    
    veiculo    = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING)
    data       = models.DateField()    
    valor      = models.FloatField()
    descricao  = models.CharField(max_length=40)
    
    def __str__(self):
        return f'{self.veiculo} - {self.valor}'
    
    class Meta:        
        db_table = 'frota"."rastreio'
    

class DespesaViagem(models.Model):    
    viagem    = models.ForeignKey(Viagem, on_delete=models.DO_NOTHING)    
    valor      = models.FloatField()
    descricao  = models.CharField(max_length=40)
    
    def __str__(self):
        return f'{self.viagem} - {self.valor}'
    
    class Meta:        
        db_table = 'frota"."despesa_viagem'


class FrotaPermissao(models.Model):
    usuario     = models.ForeignKey(User, on_delete=models.CASCADE)       
    ver_veiculo = models.BooleanField(default=True)    
    ver_manutencao = models.BooleanField(default=False)    
    ver_despesa = models.BooleanField(default=False)    
    ver_relatorio = models.BooleanField(default=False)    
    ver_carro = models.BooleanField(default=True)    
    ver_caminhao = models.BooleanField(default=True)   
    ver_abastecimento = models.BooleanField(default=True)
    ver_viagemlist = models.BooleanField(default=True) 
    ver_empilhadeira = models.BooleanField(default=False)    

    def __str__(self):
        return f'{self.usuario}'
    
    class Meta:        
        db_table = 'frota"."frota_permissao' 

        
class Manutencao(models.Model):
    MANUTENCAO = (
            ('Preventiva', 'Preventiva'),
            ('Corretiva', 'Corretiva'),             
        )
    veiculo    = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING)
    manutencao = models.CharField(max_length=40, choices=MANUTENCAO)
    valor      = models.FloatField()
    descricao  = models.CharField(max_length=40)
    created_by   = CurrentUserField()
    data_criacao = models.DateField(verbose_name="Data", default=datetime.date.today)
    

    def __str__(self):
        return f'{self.veiculo} - {self.manutencao}'
    
    class Meta:        
        db_table = 'frota"."manutencao'
