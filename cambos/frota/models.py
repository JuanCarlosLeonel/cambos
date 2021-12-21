from django.db import models
from core.models import Pessoa, Ativo

class Motorista(models.Model):
    nome    = models.ForeignKey(Pessoa, null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    cnh     = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.nome}'
    
    class Meta:        
        db_table = 'frota"."motorista' 


class Veiculo(models.Model):
    descricao   = models.ForeignKey(Ativo, null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    placa       = models.CharField(max_length=20, null=True, blank=True)    

    def __str__(self):
        return f'{self.descricao}'
    
    class Meta:        
        db_table = 'frota"."veiculo'


class VeiculoAbastecimento(models.Model):
    veiculo    = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING)
    combustivel = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.veiculo} - {self.combustivel}'
    
    class Meta:        
        db_table = 'frota"."veiculo_abastecimento'


class Viagem(models.Model):
    veiculo    = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING)
    motorista  = models.ForeignKey(Motorista, on_delete=models.DO_NOTHING)
    data       = models.DateField()
    origem     = models.CharField(max_length=40)
    destino    = models.CharField(max_length=40)
    carga      = models.CharField(max_length=40)
    peso       = models.FloatField()
    km_inicial = models.IntegerField()
    km_final   = models.IntegerField()

    def __str__(self):
        return f'{self.origem} - {self.destino}'
    
    class Meta:        
        db_table = 'frota"."viagem'


class Abastecimento(models.Model):
    veiculo        = models.ForeignKey(VeiculoAbastecimento, on_delete=models.DO_NOTHING)
    data           = models.DateField()        
    valor_unitario = models.FloatField()
    quantidade     = models.FloatField()
    
    def __str__(self):
        return f'{self.veiculo}'
    
    class Meta:        
        db_table = 'frota"."abastecimento'


class Corrida(models.Model):
    veiculo    = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING)
    motorista  = models.CharField(max_length=40)
    data       = models.DateField()    
    km_inicial = models.IntegerField()
    km_final   = models.IntegerField()
    observacao = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return f'{self.veiculo} - {self.motorista}'
    
    class Meta:        
        db_table = 'frota"."corrida'


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
