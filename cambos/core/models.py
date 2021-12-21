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


class OFICINA(models.Model):    
    choice = models.CharField(max_length=154, unique=True, verbose_name='Oficina')
    
    def __str__(self):
        return f'{self.choice}'


class ACABAMENTO(models.Model):
    choice = models.CharField(max_length=154, unique=True)
    
    def __str__(self):
        return f'{self.choice}'    


class User(AbstractUser):
    setor     = models.ForeignKey(Setor, null=True, blank=True, on_delete=models.SET_NULL)
    textil    = models.BooleanField(default=False)
    confeccao = models.BooleanField(default=False)
    frota     = models.BooleanField(default=False)


class Pessoa(models.Model):    
    id = models.AutoField(db_column='id', primary_key=True)
    matricula = models.CharField(db_column='matriculacolaborador', max_length=10, blank=True)      
    nome = models.CharField(db_column='nomecolaborador', max_length=50, blank=True)      

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


