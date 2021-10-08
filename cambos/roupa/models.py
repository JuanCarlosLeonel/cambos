from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from jsonfield import JSONField
from core.models import User

class API(models.Model):
    api = JSONField()    


class PCP(models.Model):    
    pcp = JSONField()


class Track(models.Model):    
    pcp = JSONField()


class Calendario(models.Model):    
    nome    = models.CharField(max_length=18)

    def __str__(self):
        return f'{self.nome}'
    
    class Meta:
        verbose_name_plural = "Calendário"


class DiasCalendario(models.Model):
    calendario    = models.ForeignKey(Calendario, on_delete=models.CASCADE)
    data = models.DateField()

    def __str__(self):
        return f'{self.calendario} - {self.data}'
    

class Processo(models.Model):
    nome           = models.CharField(max_length=18)    
    ordem_esperada = models.IntegerField()
    recorrente     = models.BooleanField(default=False)
    status_spi     = models.IntegerField(null=True,blank=True) 

    def __str__(self):
        return f'{self.nome}'


class TAG(models.Model):
    nome = models.CharField(max_length=154, unique=True)
    
    def __str__(self):
        return f'{self.nome}'


class Etapa(models.Model):
    LINHA_CHOICES = (
            ('Leve', 'Leve'),
            ('Pesada', 'Pesada'),             
            ('Pesada Modinha', 'Pesada Modinha'),                         
        )
    SCORE_CHOICES = (
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            )
    processo   = models.ForeignKey(Processo, on_delete=models.CASCADE)
    calendario = models.ForeignKey(Calendario, null=True, on_delete=models.SET_NULL)
    nome       = models.CharField(max_length=18,unique=True)
    interno    = models.BooleanField(default=True)
    capacidade = models.IntegerField()
    linha      = models.CharField(max_length=20, choices=LINHA_CHOICES, null=True)
    tag        = models.ManyToManyField(TAG, blank=True)
    nick_spi   = models.CharField(max_length=20, null=True, blank=True)
    score      = models.CharField(max_length=2, choices=SCORE_CHOICES, null=True)
    padrao     = models.BooleanField(default=False, verbose_name='Padrão')

    def __str__(self):
        return f'{self.nome}'
        

class Pedido(models.Model):
    lacre = models.IntegerField(unique=True, blank=False)
    tag   = models.ManyToManyField(TAG, blank=True)

    def __str__(self):
        return f'{self.lacre}'


class PedidoTrack(models.Model):    
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    lacre = models.IntegerField(default=0)


class RoupaBot(models.Model):    
    user_id    = models.IntegerField(unique=True)
    user_nome  = models.CharField(max_length=30)    
    costura    = models.ManyToManyField(Etapa, blank=True)
    lavanderia = models.BooleanField(default=False)    
    expedicao  = models.BooleanField(default=False)    
    geral      = models.BooleanField(default=False)
    ativo      = models.BooleanField(default=True)
    usuario       = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return f'{self.user_nome}'
