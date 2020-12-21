from django.db import models
from django_currentuser.db.models import CurrentUserField
from django.contrib.auth.models import AbstractUser

### Geral ###

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
        )
    nome    = models.CharField(max_length=20)
    divisao = models.CharField(max_length=20, choices=DIVISAO_CHOICES, verbose_name='Divisão')

    def __str__(self):
        return f'{self.nome}'
    
    class Meta:
        verbose_name_plural = "Setores"


class User(AbstractUser):
    setor = models.ForeignKey(Setor, null=True, blank=True, on_delete=models.SET_NULL)

    



