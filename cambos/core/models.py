from django.db import models
from django.contrib.auth.models import AbstractUser


class Periodo(models.Model):
    periodo = models.DateField(verbose_name='Período')
    nome    = models.CharField(max_length=18, default="-")

    def __str__(self):
        return f'{self.periodo}'
    
    class Meta:
        verbose_name_plural = "Período"


class Setor(models.Model):
    DIVISAO_CHOICES = (
            ('Têxtil', 'Têxtil'),
            ('Confecção', 'Confecção'),             
            ('Geral', 'Geral'),             
        )
    nome    = models.CharField(max_length=20)
    divisao = models.CharField(max_length=20, choices=DIVISAO_CHOICES, verbose_name='Divisão')

    def __str__(self):
        return f'{self.nome}'
    
    class Meta:
        verbose_name_plural = "Setores"

    
class Bot(models.Model):    
    token   = models.CharField(max_length=46)
    horas   = models.IntegerField(default=0)
    minutos = models.IntegerField(default=0)
    ativo   = models.BooleanField(default=False)


class User(AbstractUser):
    setor     = models.ForeignKey(Setor, null=True, blank=True, on_delete=models.SET_NULL)
    textil    = models.BooleanField(default=False)
    confeccao = models.BooleanField(default=False)
    frota     = models.BooleanField(default=False)


class Pessoa(models.Model):    
    id = models.AutoField(db_column='id', primary_key=True)
    matricula = models.CharField(db_column='matriculacolaborador', max_length=10, blank=True)      
    nome = models.CharField(db_column='nomecolaborador', max_length=50, blank=True)
    status = models.CharField(db_column='status',max_length=1)      

    def __str__(self):
        return f'{self.nome} ({self.matricula})'

    class Meta:
        managed = False
        db_table = 'souzacambos"."colaboradors' 


class Ativo(models.Model):    
    id = models.AutoField(db_column='id', primary_key=True)
    descricao = models.CharField(db_column='descricao', max_length=70, blank=True)      

    def __str__(self):
        return self.descricao

    class Meta:
        managed = False
        db_table = 'souzacambos"."compras_produtos' 


class SolicitacaoViagem(models.Model):
    id = models.AutoField(db_column='id',primary_key=True)
    endereco_id = models.IntegerField(db_column='endereco_id')
    user_id = models.IntegerField(db_column='user_id')
    compras_pedido_id = models.IntegerField(db_column='compras_pedido_id',null=True)
    data_prevista = models.DateField(db_column='data_prevista')
    tipo = models.CharField(db_column='tipo',max_length=1)
    origem = models.CharField(db_column='origem',max_length=1)
    situacao = models.CharField(db_column='situacao',max_length=1)
    prioridade = models.CharField(db_column='prioridade',max_length=1)
    peso = models.FloatField(db_column='peso')
    data_solicitacao = models.DateTimeField(db_column='data_solicitacao')
    data_atendimento = models.DateTimeField(db_column='data_atendimento',null=True)
    data_finalizacao = models.DateTimeField(db_column='data_finalizacao',null=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        managed = False
        db_table = 'souzacambos"."viagem_solicitacoes'


class Users(models.Model):
    id = models.AutoField(db_column='id',primary_key=True)
    name = models.CharField(db_column='name',max_length=45)


class Enderecos(models.Model):
    id = models.AutoField(db_column='id',primary_key=True)
    compras_fornecedor_id = models.IntegerField(db_column='compras_fornecedor_id',null=True)
    endereco = models.CharField(db_column='endereco',max_length=80)
    bairro = models.CharField(db_column='bairro',max_length=45)
    cidade = models.CharField(db_column='cidade',max_length=45)
    uf = models.CharField(db_column='uf',max_length=2)
    cep = models.CharField(db_column='cep',max_length=8)
    created_at = models.DateTimeField(db_column='created_at',null=True)
    updated_at = models.DateTimeField(db_column='updated_at',null=True)

    def __str__(self):
        return f'{self.endereco}'

    class Meta:
        managed = False
        db_table = 'souzacambos"."enderecos'

