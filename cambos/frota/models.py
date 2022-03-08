import math
from statistics import mode
from time import time
from django import db
from django.db import IntegrityError, models
from django.db.models.constraints import CheckConstraint, UniqueConstraint
from django.db.models import Q, F
from core.models import Pessoa, Ativo, User
from django_currentuser.db.models import CurrentUserField
import datetime
from django.core.exceptions import ValidationError


class Veiculo(models.Model):
    descricao   = models.ForeignKey(Ativo, null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    placa       = models.CharField(max_length=20, null=True, blank=True)    
    caminhao    = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.descricao}'
    
    class Meta:        
        db_table = 'frota"."veiculo'

class Motorista(models.Model):
    nome = models.ForeignKey(Pessoa, null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    cnh = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.nome}'

    class Meta:        
        db_table = 'frota"."motorista' 

class Viagem(models.Model):
    veiculo      = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING, blank=True)
    motorista    = models.ForeignKey(Pessoa, on_delete=models.DO_NOTHING, db_constraint=False)
    motorista2   = models.ForeignKey(Pessoa, on_delete=models.DO_NOTHING, db_constraint=False, related_name='motorista2', blank=True, null=True)
    ajudante     = models.ForeignKey(Pessoa, on_delete=models.DO_NOTHING, db_constraint=False, related_name='ajudante', blank=True, null=True)
    data_inicial = models.DateField(blank=True, null=True)
    data_final   = models.DateField(blank=True, null=True)
    hora_inicial = models.TimeField(blank=True, null=True)
    hora_final   = models.TimeField(blank=True, null=True)
    origem       = models.CharField(max_length=40, blank=True)
    destino      = models.CharField(max_length=250)
    carga        = models.CharField(max_length=40, blank=True)
    peso         = models.FloatField(blank=True, null=True)
    km_inicial   = models.IntegerField(blank=True, null=True)
    km_final     = models.IntegerField(blank=True, null=True)
    created_by   = CurrentUserField()
    data_criacao = models.DateField(verbose_name="Data", default=datetime.date.today)
    
    class Meta:        
        constraints = [
            models.CheckConstraint(check=Q(data_final__gte=F('data_inicial')), name="datafinal_menor_datainicial"),
            models.CheckConstraint(check=Q(km_final__gt=F('km_inicial')), name="kmfinal_menor_kminicial"),
            models.UniqueConstraint(fields=['veiculo','data_inicial','hora_inicial'], name="Ja Reservado para esta data,verificar os horarios")
            # models.UniqueConstraint(fields=['veiculo'], condition=Q(data_final = True) & Q(hora_final = True) & Q(km_final = None), name="Ja Reservado para esta data,verificar os horarios")
        ]
        db_table = 'frota"."viagem'
        ordering = ["-data_criacao"]

    def clean(self):
        if self.data_final == None:
            pass
        elif self.data_final < self.data_inicial:
            raise ValidationError({'data_final':('Data final tem que ser maior que data inicial')})
        if self.km_final == None:
            pass
        elif self.km_final <= self.km_inicial:
            raise ValidationError({'km_final':('Km final tem que ser maior que Km inicial.')})

    def __str__(self):
        return f'{self.origem} - {self.destino}'

    @property
    def kmfinalmenosinicial(self):
        if self.km_final is None:
            pass
        else:
            return (self.km_final - self.km_inicial)

    @property
    def diagasto(self):
        if self.data_final is None:
            pass
        elif (self.data_final - self.data_inicial).days == 0:
            pass
        elif self.hora_final < self.hora_inicial:
            return (self.data_final - self.data_inicial).days -1
        else:
            return (self.data_final - self.data_inicial).days

    @property
    def horagasto(self):
        from datetime import datetime, date
        if self.hora_final is None:
            pass
        else:
            return datetime.combine(date.today(),self.hora_final) - datetime.combine(date.today(),self.hora_inicial)


class Abastecimento(models.Model):
    COMBUSTIVEL = (
            ('Diesel', 'Diesel'),
            ('Gasolina', 'Gasolina'),             
            ('Álcool', 'Álcool'),                         
        )
    interno = models.BooleanField(default=False)
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
    km = models.IntegerField(blank=True, null=True)
    manutencao = models.CharField(max_length=40, choices=MANUTENCAO)
    valor      = models.FloatField()
    descricao  = models.CharField(max_length=40)
    created_by   = CurrentUserField()
    data_criacao = models.DateField(verbose_name="Data", default=datetime.date.today)
    

    def __str__(self):
        return f'{self.veiculo} - {self.manutencao}'
    
    class Meta:        
        db_table = 'frota"."manutencao'
