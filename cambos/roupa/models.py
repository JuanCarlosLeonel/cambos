from django.db import models


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
    status_spi     = models.IntegerField() 

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
    processo   = models.ForeignKey(Processo, on_delete=models.CASCADE)
    calendario = models.ForeignKey(Calendario, null=True, blank=True, on_delete=models.SET_NULL)
    nome       = models.CharField(max_length=18)
    interno    = models.BooleanField(default=True)
    capacidade = models.IntegerField()
    linha      = models.CharField(max_length=20, choices=LINHA_CHOICES, null=True, blank=True)
    tag        = models.ManyToManyField(TAG, blank=True)
    nick_spi   = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.nome}'
