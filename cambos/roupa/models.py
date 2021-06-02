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
    interno        = models.BooleanField(default=True)
    ordem_esperada = models.IntegerField()
    recorrente     = models.BooleanField(default=False)
    status_spi     = models.IntegerField() 

    def __str__(self):
        return f'{self.nome}'


class Etapa(models.Model):
    processo   = models.ForeignKey(Processo, on_delete=models.CASCADE)
    calendario = models.ForeignKey(Calendario, null=True, blank=True, on_delete=models.SET_NULL)
    nome       = models.CharField(max_length=18)
    capacidade = models.IntegerField()
    nick_spi   = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.nome}'
