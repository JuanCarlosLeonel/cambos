import math
from pyexpat import model
from statistics import mode
from time import time
from django import db
from django.db import IntegrityError, models
from django.db.models.constraints import CheckConstraint, UniqueConstraint
from django.db.models import Q, F
from core.models import Pessoa, Ativo, User , UserCompras, Enderecos, SetoresPortal
from django_currentuser.db.models import CurrentUserField
import datetime
from django.core.exceptions import ValidationError


class Veiculo(models.Model):
    descricao   = models.ForeignKey(Ativo, null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    placa       = models.CharField(max_length=20, null=True, blank=True)    
    caminhao    = models.BooleanField(default=False)
    gerador     = models.BooleanField(default=False)
    trator      = models.BooleanField(default=False)
    empilhadeira= models.BooleanField(default=False)

    def __str__(self):
        return f'{self.descricao}'
    
    class Meta:        
        db_table = 'frota"."veiculo'

class Motorista(models.Model):
    nome = models.ForeignKey(Pessoa, null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    cnh = models.CharField(max_length=20)
    empilhadeirista = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.nome}'

    class Meta:        
        db_table = 'frota"."motorista' 

class Viagem(models.Model):
    TIPOVIAGEM = (
            ('Manutençao', 'Manutenção'),
            ('Viagem', 'Viagem'),                                     
        )
    tipo = models.CharField(max_length=40, choices=TIPOVIAGEM,default='Viagem')
    veiculo      = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING, blank=True)
    motorista    = models.ForeignKey(Pessoa, on_delete=models.DO_NOTHING, db_constraint=False)
    motorista2   = models.ForeignKey(Pessoa, on_delete=models.DO_NOTHING, db_constraint=False, related_name='motorista2', blank=True, null=True)
    ajudante     = models.ForeignKey(Pessoa, on_delete=models.DO_NOTHING, db_constraint=False, related_name='ajudante', blank=True, null=True)
    data_inicial = models.DateField(blank=True, null=True)
    data_final   = models.DateField(blank=True, null=True)
    hora_inicial = models.TimeField(blank=True, null=True)
    hora_final   = models.TimeField(blank=True, null=True)
    origem       = models.CharField(max_length=40, blank=True)
    destino      = models.CharField(max_length=250)
    carga        = models.CharField(max_length=40, blank=True)
    peso         = models.FloatField(blank=True, null=True)
    km_inicial   = models.IntegerField(blank=True, null=True)
    km_final     = models.IntegerField(blank=True, null=True)
    created_by   = CurrentUserField()
    data_criacao = models.DateField(verbose_name="Data", default=datetime.date.today)
    
    class Meta:        
        constraints = [
            models.CheckConstraint(check=Q(data_final__gte=F('data_inicial')), name="datafinal_menor_datainicial"),
            models.CheckConstraint(check=Q(km_final__gt=F('km_inicial')), name="kmfinal_menor_kminicial"),
            models.UniqueConstraint(fields=['veiculo','data_inicial','hora_inicial'], name="Ja Reservado para esta data,verificar os horarios")
            # models.UniqueConstraint(fields=['veiculo'], condition=Q(data_final = True) & Q(hora_final = True) & Q(km_final = None), name="Ja Reservado para esta data,verificar os horarios")
        ]
        db_table = 'frota"."viagem'
        ordering = ["-data_criacao"]

    def clean(self):
        if self.data_final == None:
            pass
        elif self.data_final < self.data_inicial:
            raise ValidationError({'data_final':('Data final tem que ser maior que data inicial')})
        if self.km_final == None:
            pass
        elif self.km_final <= self.km_inicial:
            raise ValidationError({'km_final':('Km final tem que ser maior que Km inicial.')})

    def __str__(self):
        return f'{self.origem} - {self.destino}'

    @property
    def kmfinalmenosinicial(self):
        if self.km_final is None:
            pass
        else:
            return (self.km_final - self.km_inicial)

    @property
    def diagasto(self):
        if self.data_final is None:
            pass
        elif (self.data_final - self.data_inicial).days == 0:
            pass
        elif self.hora_final < self.hora_inicial:
            return (self.data_final - self.data_inicial).days -1
        else:
            return (self.data_final - self.data_inicial).days

    @property
    def horagasto(self):
        from datetime import datetime, date
        if self.hora_final is None:
            pass
        else:
            return datetime.combine(date.today(),self.hora_final) - datetime.combine(date.today(),self.hora_inicial)


class Abastecimento(models.Model):
    COMBUSTIVEL = (
            ('Diesel', 'Diesel'),
            ('Gasolina', 'Gasolina'),             
            ('Álcool', 'Álcool'),                         
        )
    RESPONSAVEL = (
            ('JOAO LUIS SEMBOLONI', 'JOAO LUIS SEMBOLONI'),
            ('ANTONIO PEDRO DE ARAUJO FILHO', 'ANTONIO PEDRO DE ARAUJO FILHO'),
            ('ISAAC DA SILVA HERCULANO', 'ISAAC DA SILVA HERCULANO'),
            ('PAULO VITOR TAVEIRA', 'PAULO VITOR TAVEIRA'),
            ('JONATHAN CARVALHO XIMENES', 'JONATHAN CARVALHO XIMENES'),
            ('VALDIR DONIZETTI FERREIRA', 'VALDIR DONIZETTI FERREIRA'),
            ('LINDEMBERG RODRIGUES DA SILVA', 'LINDEMBERG RODRIGUES DA SILVA'),
    )
    interno = models.BooleanField(default=False)
    veiculo        = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING, blank=True)
    combustivel = models.CharField(max_length=40, choices=COMBUSTIVEL)
    data           = models.DateField()        
    valor_unitario = models.FloatField(null=True,blank=True)
    quantidade     = models.FloatField()
    responsavel    = models.CharField(max_length=40, null=True, choices=RESPONSAVEL)

    def __str__(self):
        return f'{self.veiculo}'
    
    class Meta:        
        db_table = 'frota"."abastecimento'

#buscar informações do abastecimento interno na tabela estoque/souzacambos
class EstoqueDiesel(models.Model):
    id = models.AutoField(db_column='id',primary_key=True)
    almoxarifado_id = models.IntegerField(db_column='almoxarifado_id')
    produto_id = models.IntegerField(db_column='produto_id')
    user_id = models.IntegerField(db_column='user_id')
    quantidade = models.FloatField(db_column='quantidade')
    valor_unico = models.FloatField(db_column='valor_unico')
    created_at = models.DateTimeField(db_column='created_at')
    updated_at = models.DateTimeField(db_column='updated_at')

    class Meta:
        managed = False
        db_table = 'souzacambos"."estoque'

#para quando houver um abastecimento interno informar os dados de onde veio a movimentação
class Movimentacoes(models.Model):
    id = models.AutoField(db_column='id',primary_key=True)
    estoque_id = models.IntegerField(db_column='estoque_id')
    user_id = models.IntegerField(db_column='user_id')
    tipo = models.CharField(db_column='tipo', max_length=1)
    descricao = models.CharField(db_column='descricao', max_length=191)
    quantidade = models.FloatField(db_column='quantidade')
    valor_unico = models.FloatField(db_column='valor_unico')
    saldo_anterior = models.FloatField(db_column='saldo_anterior') 
    saldo_atual = models.FloatField(db_column='saldo_atual')
    created_at = models.DateTimeField(db_column='created_at')
    class Meta:
        managed = False
        db_table = 'souzacambos"."movimentacoes'

class SolicitacaoViagem(models.Model):
    TIPO = (
            ('1', 'Coleta'),
            ('2', 'Entrega'),  
            ('3', 'Coleta Direta'),
            ('4', 'Entrada Direta'),                                                                     
        )
    ORIGEM = (
            ('1', 'Compras'),
            ('2', 'Outros'),
    )
    SITUACAO = (
            ('1', 'Aguardando Atendimento'),
            ('2', 'Em Atendimento'),
            ('3', 'Finalizado'),
    )
    PRIORIDADE = (
            ('1', 'Normal'),
            ('2', 'Urgente'),
    )
    id = models.AutoField(db_column='id',primary_key=True)
    endereco = models.ForeignKey(Enderecos,db_column='endereco_id',on_delete=models.DO_NOTHING)
    user = models.ForeignKey(UserCompras,db_column='user_id',on_delete=models.DO_NOTHING)
    compras_pedido_id = models.IntegerField(db_column='compras_pedido_id',null=True)
    data_prevista = models.DateField(db_column='data_prevista')
    tipo = models.CharField(db_column='tipo',choices=TIPO,max_length=1)
    origem = models.CharField(db_column='origem',choices=ORIGEM,max_length=1,default='2')
    situacao = models.CharField(db_column='situacao',choices=SITUACAO,max_length=1,default='1')
    prioridade = models.CharField(db_column='prioridade',choices=PRIORIDADE,max_length=1)
    quantidade = models.IntegerField(db_column='quantidade',null=True,blank=True)
    peso = models.FloatField(db_column='peso')
    produtos = models.TextField()
    horaentrega_coleta = models.TextField(db_column='horario',null=True)
    data_solicitacao = models.DateTimeField(db_column='data_solicitacao')
    data_atendimento = models.DateTimeField(db_column='data_atendimento',null=True)
    data_finalizacao = models.DateTimeField(db_column='data_finalizacao',null=True)
    has_item = False

    def set_has_item(self, value = False):
        self.has_item = value

    def __str__(self):
        return f'{self.id}'

    class Meta:
        managed = False
        db_table = 'frota"."viagem_solicitacoes'

class PedidoItem(models.Model):
    compras_pedido_id = models.IntegerField(db_column='compras_pedido_id',null=True)
    compras_produto_id = models.IntegerField(db_column='compras_produto_id', null=True)
    
    def __str__(self):
        return str(self.compras_pedido_id)

    class Meta:
        managed = False
        db_table = 'souzacambos"."compras_pedido_items' 


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


class FrotaPermissao(models.Model):
    usuario     = models.ForeignKey(User, on_delete=models.CASCADE)       
    ver_veiculo = models.BooleanField(default=True)    
    ver_manutencao = models.BooleanField(default=False)    
    ver_despesa = models.BooleanField(default=False)    
    ver_relatorio = models.BooleanField(default=False)    
    ver_carro = models.BooleanField(default=True)    
    ver_caminhao = models.BooleanField(default=True)   
    ver_abastecimento = models.BooleanField(default=True)
    ver_viagemlist = models.BooleanField(default=True) 
    ver_empilhadeira = models.BooleanField(default=False)    
    ver_trator = models.BooleanField(default=False)  
    ver_gerador = models.BooleanField(default=False)  
    ver_solicitacao = models.BooleanField(default=False)
    ver_controlevisitas = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.usuario}'
    
    class Meta:        
        db_table = 'frota"."frota_permissao' 

        
class Manutencao(models.Model):
    MANUTENCAO = (
            ('Preventiva', 'Preventiva'),
            ('Corretiva', 'Corretiva'),             
        )
    veiculo    = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING)
    km = models.IntegerField(blank=True, null=True)
    manutencao = models.CharField(max_length=40, choices=MANUTENCAO)
    valor      = models.FloatField()
    descricao  = models.CharField(max_length=40)
    created_by   = CurrentUserField()
    data_criacao = models.DateField(verbose_name="Data", default=datetime.date.today)
    

    def __str__(self):
        return f'{self.veiculo} - {self.manutencao}'
    
    class Meta:        
        db_table = 'frota"."manutencao'


class ItemViagem(models.Model):    
    id = models.AutoField(primary_key=True)
    viagem = models.ForeignKey(Viagem,on_delete=models.DO_NOTHING, db_constraint=False)     
    viagem_solicitacao = models.ForeignKey(SolicitacaoViagem,on_delete=models.DO_NOTHING, db_constraint=False)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        managed = False
        db_table = 'frota"."viagem_itens' 


class FrotaBot(models.Model):
    user_id       = models.BigIntegerField(unique=True)
    user_nome     = models.CharField(max_length=30)    
    ver_logistica     = models.BooleanField(default=False)
    ver_relatorioveiculos     = models.BooleanField(default=False)
    ativo         = models.BooleanField(default=True)
    usuario       = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.user_nome}'

#para a portaria
class ControleVisitantes(models.Model):
    data = models.DateField()
    nome = models.CharField(max_length=45)
    documento = models.CharField(max_length=12)
    hora_inicial = models.TimeField(blank=True, null=True)
    hora_final   = models.TimeField(blank=True, null=True)
    responsavel = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.nome}'

    class Meta:        
        db_table = 'frota"."controle_visitante'

#EMPILHADEIRAS
class Servicos(models.Model):
    TIPOSERVICO= (
            ('Ordem Serviço', 'Ordem Serviço'),
            ('Manutençao', 'Manutenção'),            
        )
    TIPOMANUTENCAO= (
            ('Preventiva', 'Preventiva'),
            ('Corretiva', 'Corretiva'),       
        )
    descricao = models.CharField(max_length=80)
    quantidade = models.IntegerField(blank=True, null=True)
    motorista = models.ForeignKey(Motorista,on_delete=models.DO_NOTHING, db_constraint=False)
    empilhadeira = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING, db_constraint=False)
    data_inicial = models.DateField(blank=True, null=True)
    data_final   = models.DateField(blank=True, null=True)
    hora_inicial = models.TimeField(blank=True, null=True)
    hora_final   = models.TimeField(blank=True, null=True)
    tipo_servico = models.CharField(choices=TIPOSERVICO, max_length=20, null=True)
    tipo_manutencao = models.CharField(choices=TIPOMANUTENCAO, max_length=20, null=True)

    def __str__(self):
        return f'{self.descricao}'

    class Meta:        
        db_table = 'frota"."empilhadeira_servico'


class Ordem(models.Model):
    SITUACAO= (
            ('1', 'Aberto'),
            ('2', 'Em atendimento'),    
            ('3', 'Finalizado'),          
        )
    setor = models.ForeignKey(SetoresPortal,on_delete=models.SET_NULL, blank=True, null=True)
    descricao = models.CharField(max_length=80)
    quantidade = models.IntegerField(blank=True, null=True)
    situacao = models.CharField(choices=SITUACAO, max_length=1)
    servico = models.ForeignKey(Servicos,on_delete=models.DO_NOTHING, null=True)
    observacao = models.CharField(max_length=80,null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return f'{self.descricao}'

    class Meta:        
        db_table = 'frota"."empilhadeira_ordem'


class ManutencaoEmpilhadeira(models.Model):
    empilhadeira = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, blank=True, null=True)
    botijaoreposto = models.CharField(max_length=2)
    botijaoutilizado = models.CharField(max_length=2)
    responsavel = models.TextField(max_length=100)

    def __str__(self):
        return f'{self.empilhadeira}'

    class Meta:        
        db_table = 'frota"."empilhadeira_manutencao'


