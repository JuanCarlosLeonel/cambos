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
    TIPO_BOT = (
            ('PCP', 'PCP'),
            ('Qualidade', 'Qualidade'),                                     
            ('Frota', 'Frota'),                                     
        )
    nome    = models.CharField(max_length=20, choices=TIPO_BOT, default='PCP')
    token   = models.CharField(max_length=46)
    horas   = models.IntegerField(default=0)
    minutos = models.IntegerField(default=0)
    ativo   = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nome}'


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

class SetoresPortal(models.Model):
    id = models.AutoField(db_column='id', primary_key = True)
    nome = models.CharField(db_column='nome',max_length=80, blank=True)

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        managed = False
        db_table = 'souzacambos"."setores' 




class Ativo(models.Model):    
    id = models.AutoField(db_column='id', primary_key=True)
    descricao = models.CharField(db_column='descricao', max_length=70, blank=True)      

    def __str__(self):
        return self.descricao

    class Meta:
        managed = False
        db_table = 'souzacambos"."compras_produtos' 



class UserCompras(models.Model):
    id = models.AutoField(db_column='id',primary_key=True)
    name = models.CharField(db_column='name',max_length=45)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'souzacambos"."users'


class Enderecos(models.Model):
    id = models.AutoField(db_column='id',primary_key=True)
    tipo = models.CharField(db_column='tipo',max_length=1,default=1)
    compras_fornecedor_id = models.IntegerField(db_column='compras_fornecedor_id',null=True)
    endereco = models.CharField(db_column='endereco',max_length=80)
    bairro = models.CharField(db_column='bairro',max_length=45)
    numero = models.CharField(db_column='numero',max_length=40)
    cidade = models.CharField(db_column='cidade',max_length=45)
    uf = models.CharField(db_column='uf',max_length=2)
    cep = models.CharField(db_column='cep',max_length=8)
    created_at = models.DateTimeField(db_column='created_at',null=True)
    updated_at = models.DateTimeField(db_column='updated_at',null=True)

    def __str__(self):
        return f'{self.endereco,self.numero,self.bairro,self.cidade}'

    class Meta:
        managed = False
        db_table = 'frota"."enderecos'

