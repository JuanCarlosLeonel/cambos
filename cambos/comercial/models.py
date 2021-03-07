from django.db import models
from django_currentuser.db.models import CurrentUserField
import datetime


class Comercial(models.Model):    
    nome    = models.CharField(max_length=18)

    def __str__(self):
        return f'{self.nome}'
    
    class Meta:
        verbose_name_plural = "Comercial"


class Cliente(models.Model):
    comercial   = models.ForeignKey(Comercial, on_delete=models.SET_NULL, null=True)
    nome        = models.CharField(max_length=40)
    cota_mensal = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.nome} ({self.comercial})'


class CustoManipulacao(models.Model):
    cliente   = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=140)
    custo     = models.FloatField()

    def __str__(self):
        return f'{self.cliente} - {self.custo}'
      

class Cotacao(models.Model):
    SITUACAO_CHOICES = (
        ('Aberta', 'Aberta'),
        ('Fechada', 'Fechada'),             
    )
    cliente       = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    descricao     = models.CharField(max_length=40, verbose_name="Descrição")
    representante = CurrentUserField()    
    data_criacao  = models.DateField(verbose_name="Data", default=datetime.date.today)
    data_entrega  = models.DateField(verbose_name="Entrega Pedido", blank=True)
    notas         = models.CharField(max_length=140, blank=True, null=True)
    situacao      = models.CharField(max_length=50, verbose_name="Situação", choices=SITUACAO_CHOICES, default="Aberta")

    def __str__(self):
        return f'{self.cliente} ({self.descricao})'


class Tecido(models.Model):
    nome       = models.CharField(max_length=140, unique=True)
    composicao = models.CharField(max_length=140, verbose_name="Composição")
    peso       = models.FloatField()
    inativo    = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nome}'


class PrecoTecido(models.Model):
    tecido        = models.ForeignKey(Tecido, on_delete=models.CASCADE)
    data          = models.DateField(default=datetime.date.today)
    valor_consumo = models.FloatField()
    valor_venda   = models.FloatField()

    def __str__(self):
        return f'{self.tecido} - {self.data}'


class PontuacaoProducao(models.Model):
    pontuacao     = models.FloatField(verbose_name="Pontuação", unique=True)
    valor_interno = models.FloatField()
    valor_externo = models.FloatField()

    def __str__(self):
        return f'{self.pontuacao}'


class Produto(models.Model):
    cod        = models.IntegerField(unique=True)
    ref        = models.IntegerField()
    tecido     = models.ForeignKey(Tecido, on_delete=models.PROTECT)
    pontos     = models.ForeignKey(PontuacaoProducao, on_delete=models.PROTECT)
    consumo    = models.FloatField()
    lavanderia = models.FloatField()
    acabamento = models.FloatField()
    insumos    = models.FloatField()

    def __str__(self):
        return f'{self.cod}'


class ItemCotacao(models.Model):
    cotacao      = models.ForeignKey(Cotacao, on_delete=models.CASCADE)
    produto      = models.ForeignKey(Produto, on_delete=models.PROTECT, blank=True)
    ref_cliente  = models.CharField(blank=True, max_length=10)
    descricao    = models.CharField(max_length=30, verbose_name="Descrição")
    quantidade   = models.IntegerField(blank=True)
    target       = models.FloatField(blank=True)
    data_entrega = models.DateField(blank=True, verbose_name="Entrega")
    notas         = models.CharField(max_length=140, blank=True, null=True)

    def __str__(self):
        return f'{self.cod}'


class Proposta(models.Model):
    item        = models.ForeignKey(ItemCotacao, on_delete=models.CASCADE)
    tecido      = models.ForeignKey(Tecido, on_delete=models.PROTECT)
    pontos      = models.ForeignKey(PontuacaoProducao, on_delete=models.PROTECT)
    consumo     = models.FloatField()
    lavanderia  = models.FloatField()
    acabamento  = models.FloatField()
    insumos     = models.FloatField()
    manipulacao = models.ForeignKey(CustoManipulacao, on_delete=models.PROTECT)
    operacional = models.FloatField()
    tributos    = models.FloatField()
    total       = models.FloatField()
