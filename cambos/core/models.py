from django.db import models
from django.db.models.deletion import SET_NULL
from django_currentuser.db.models import CurrentUserField
from django.contrib.auth.models import AbstractUser
from comercial.models import Comercial


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


class UserBot(models.Model):
    user_id    = models.IntegerField(unique=True)
    user_nome  = models.CharField(max_length=30)
    user_tel   = models.CharField(max_length=30, blank=True)
    oficina    = models.ManyToManyField(OFICINA, blank=True)
    lavanderia = models.BooleanField(default=False)
    corte      = models.BooleanField(default=False)
    expedicao  = models.BooleanField(default=False)
    acabamento = models.ManyToManyField(ACABAMENTO, blank=True)
    geral = models.BooleanField(default=False)
    ativo   = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user_nome}'


class User(AbstractUser):
    COM_CHOICES = (
            ('Mendes Júnior', 'Mendes Júnior'),
            ('Xavantes', 'Xavantes'),             
            ('Cotton Move', 'Cotton Move'),             
            ('Geral', 'Geral'),             
        )
    setor     = models.ForeignKey(Setor, null=True, blank=True, on_delete=models.SET_NULL)
    textil    = models.BooleanField(default=False)
    confeccao = models.BooleanField(default=False)
    comercial = models.ManyToManyField(Comercial, blank=True)
    user_bot  = models.ForeignKey(UserBot, null=True, blank=True, on_delete=SET_NULL)
