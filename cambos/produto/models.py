from django.db import models
from core.models import Setor, Periodo
from django_currentuser.db.models import CurrentUserField
import datetime

class Desempenho(models.Model):
    UN_CHOICES = (
            ('kg', 'kg'),
            ('m', 'm'),             
        )
    setor                   = models.ForeignKey(Setor, on_delete=models.CASCADE)
    periodo                 = models.ForeignKey(Periodo, on_delete=models.CASCADE)    
    capacidade_total        = models.IntegerField(blank=True, null=True, verbose_name='Capacidade Total')
    dias_trabalhados        = models.FloatField(blank=True, null=True, verbose_name='Dias Trabalhados')
    total_planejado         = models.IntegerField(blank=True, null=True, verbose_name='Total Planejado')
    headcount               = models.FloatField(blank=True, null=True, verbose_name='nº Colaboradores')
    expedidores             = models.FloatField(blank=True, null=True, verbose_name='nº Expedidores')
    revisores               = models.FloatField(blank=True, null=True, verbose_name='nº Revisores')
    setup                   = models.FloatField(blank=True, null=True)
    carga_descarga          = models.FloatField(blank=True, null=True)
    manutencao_corretiva    = models.FloatField(blank=True, null=True)
    manutencao_preventiva   = models.FloatField(blank=True, null=True)
    total_alvejado          = models.FloatField(blank=True, null=True, verbose_name='Total Alvejado')
    total_chamuscado        = models.FloatField(blank=True, null=True, verbose_name='Total Chamuscado')
    total_expedido          = models.FloatField(blank=True, null=True, verbose_name='Total Expedido')
    total_recebido          = models.FloatField(blank=True, null=True, verbose_name='Total Recebido')
    total_tingido           = models.FloatField(blank=True, null=True, verbose_name='Total Tingido')
    tempo_total_atendimento = models.FloatField(blank=True, null=True, verbose_name='Tempo Total de Atendimento')
    created_by              = CurrentUserField()
    data_criacao            = models.DateField(verbose_name="Data", default=datetime.date.today)

    def __str__(self):
        return f'{self.setor}'
    
    class Meta:
        verbose_name_plural = "Desempenho"


class Material(models.Model):
    UN_CHOICES = (
        ('kg', 'kg'),
        ('m', 'm'),             
    )

    TIPO_CHOICES = (
            ('Insumo', 'Insumo'),
            ('Material', 'Material'),                         
            ('Refugo', 'Refugo'),                         
        )
    
    ORIGEM_CHOICES = (
            ('Compra', 'Compra'),
            ('Fiação', 'Fiação'),             
            ('Entrelaçadeira', 'Entrelaçadeira'),             
            ('Tingimento', 'Tingimento'),
            ('Tecelagem', 'Tecelagem'),
            ('Urdideira', 'Urdideira'),             
            ('Perda', 'Perda'),             
        )
    cod          = models.IntegerField(null=True, blank=True)
    nome         = models.CharField(max_length=110)
    origem       = models.CharField(max_length=20, choices=ORIGEM_CHOICES)
    tipo         = models.CharField(max_length=20, choices=TIPO_CHOICES)
    created_by   = CurrentUserField()
    data_criacao = models.DateField(verbose_name="Data", default=datetime.date.today)
    unidade      = models.CharField(blank=True, max_length=20, choices=UN_CHOICES)
    inativo      = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nome} - ({self.origem})'
    
    class Meta:
        verbose_name_plural = "Materiais"


class Composicao(models.Model):
    produto      = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="produto")
    material     = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="material")
    composicao   = models.FloatField()
    created_by   = CurrentUserField()
    data_criacao = models.DateField(verbose_name="Data", default=datetime.date.today)

    def __str__(self):
        return f'{self.produto}'
    
    class Meta:
        verbose_name_plural = "Composição"


class ValorCompra(models.Model):
    periodo      = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    material     = models.ForeignKey(Material, on_delete=models.CASCADE)
    valor        = models.FloatField()
    created_by   = CurrentUserField()
    data_criacao = models.DateField(verbose_name="Data", default=datetime.date.today)

    def __str__(self):
        return f'{self.material} / {self.periodo}'
    
    class Meta:
        verbose_name_plural = "Valor de Compra"


class Consumo(models.Model):
    
    periodo      = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    material     = models.ForeignKey(Material, on_delete=models.CASCADE)
    setor        = models.ForeignKey(Setor, on_delete=models.CASCADE)
    quantidade   = models.FloatField( default=0)
    created_by   = CurrentUserField()
    data_criacao = models.DateField(verbose_name="Data", default=datetime.date.today)

    def __str__(self):
        return f'{self.material} / {self.periodo}'
    
    class Meta:
        verbose_name_plural = "Consumo"

    @property
    def valor(self):
        if self.material.origem == "Compra":
            preco = 0
        else:
            preco = 10
        return preco


class Perda(models.Model):
    
    periodo      = models.ForeignKey(Periodo, on_delete=models.CASCADE)    
    setor        = models.ForeignKey(Setor, on_delete=models.CASCADE)    
    material     = models.ForeignKey(Material, on_delete=models.CASCADE, default=1)
    quantidade   = models.FloatField( default=0)
    created_by   = CurrentUserField()
    data_criacao = models.DateField(verbose_name="Data", default=datetime.date.today)

    def __str__(self):
        return f'{self.setor} / {self.periodo}'
    

class Custo(models.Model):
     
    periodo               = models.ForeignKey(Periodo, on_delete=models.CASCADE)    
    setor                 = models.ForeignKey(Setor, on_delete=models.CASCADE)    
    energia               = models.FloatField(blank=True)
    laboratorio           = models.FloatField(blank=True)
    manutencao            = models.FloatField(blank=True)
    mao_de_obra           = models.FloatField(blank=True)
    material_uso_continuo = models.FloatField(blank=True)
    vapor                 = models.FloatField(blank=True)
    agua                  = models.FloatField(blank=True)
    created_by            = CurrentUserField()
    data_criacao          = models.DateField(verbose_name="Data", default=datetime.date.today)

    def __str__(self):
        return f'{self.setor} / {self.periodo}'


class Producao(models.Model):
    
    periodo      = models.ForeignKey(Periodo, on_delete=models.CASCADE)    
    setor        = models.ForeignKey(Setor, on_delete=models.CASCADE)    
    material     = models.ForeignKey(Material, on_delete=models.CASCADE)    
    quantidade   = models.FloatField()
    created_by   = CurrentUserField()
    data_criacao = models.DateField(verbose_name="Data", default=datetime.date.today)
    
    def __str__(self):
        return f'{self.material}'

    class Meta:
        verbose_name_plural = "Produção"
