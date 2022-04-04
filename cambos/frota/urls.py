from django.urls import path
from django.views.generic.base import View

from .views import(
    Index,
    SolicitacaoMotoristaUpdate,
    VeiculoIndex,
    ViagemList,
    ViagemCreate,
    ViagemUpdate,
    ViagemDelete,    
    AbastecimentoList,
    AbastecimentoCreate,
    AbastecimentoUpdate,
    AbastecimentoDelete,
    VeiculoList,    
    RelatorioViagem,
    RelatorioViagemSolicitacao,
    RelatorioViagemCarro,
    RelatorioList,
    RelatorioAbastecimento,
    RelatorioAbastecimentoCaminhao,
    relatorio_despesa,
    relatorio_abastecimento_porveiculo,
    relatorio_despesacaminhao,
    relatorio_abastecimento_porcaminhao,
    relatorio_despesatrator,
    relatorio_abastecimento_portrator,
    relatorio_despesagerador,
    relatorio_abastecimento_porgerador,
    relatorio_manutencao_porveiculo,
    enviar,
    enviarabastecimento,
    IndexDespesas,
    ManutencaoList,
    ManutencaoCreate,
    ManutencaoUpdate,
    ManutencaoDelete,
    AbastecimentoListALL,
    ManutencaoListALL,
    SolicitacoesList,
    SolicitacaoList,
    SolicitacaoCreate,
    SolicitacaoUpdate,
    SolicitacaoDelete,
    EnderecoCreate,
    sucesso,
    ControleVisitaList,
    VisitanteCreate,
    VisitanteUpdate,
    VisitanteDelete,
    RelatorioEmpilhadeira
)

urlpatterns = [
    path('index', Index.as_view(), name='frota_index'),        
    path('veiculo_index/<str:pk>/', VeiculoIndex.as_view(), name='veiculo_index'), 
    path('relatorio_viagemcarro', RelatorioViagemCarro.as_view(), name='relatorio_viagemcarro'),
    path('relatorio_viagem',  RelatorioViagem.as_view(), name='relatorio_viagem'),
    path('relatorio_viagemsolicitacao',  RelatorioViagemSolicitacao.as_view(), name='relatorio_viagemsolicitacao'),
    path('relatorio_abastecimentocarro',  RelatorioAbastecimento.as_view(), name='relatorio_abastecimentocarro'),
    path('relatorio_abastecimentocaminhao', RelatorioAbastecimentoCaminhao.as_view(), name='relatorio_abastecimentocaminhao'),
    path('relatorio_index',  RelatorioList.as_view(), name='relatorio_index'),
    path('relatorio_empilhadeira',  RelatorioEmpilhadeira.as_view(), name='relatorio_empilhadeira'),
    path('viagem_list/<str:pk>/',  ViagemList.as_view(), name='viagem_list'),
    path('solicitacao_list/',  SolicitacaoList.as_view(), name='solicitacao_list'),
    path('visitantes_list/',  ControleVisitaList.as_view(), name='visitantes_list'),
    path('visitante_create/', VisitanteCreate.as_view(), name = 'visitante_create'),
    path('visitante_update/<str:pk>/', VisitanteUpdate.as_view(), name='visitante_update'),
    path('visitante_delete/<int:pk>/',VisitanteDelete.as_view(), name='visitante_delete_cbv'),
    path('solicitacao_create/', SolicitacaoCreate.as_view(), name = 'solicitacao_create'),
    path('endereco_create/', EnderecoCreate.as_view(), name = 'endereco_create'),
    path('solicitacaomotorista_update/<str:pk>/', SolicitacaoMotoristaUpdate.as_view(), name='solicitacaomotorista_update'), 
    path('solicitacao_update/<str:pk>/', SolicitacaoUpdate.as_view(), name='solicitacao_update'),
    path('solicitacao_delete/<int:pk>/',SolicitacaoDelete.as_view(), name='solicitacao_delete_cbv'),
    path('viagem_solicitacao_list/<int:pk>/',  SolicitacoesList.as_view(), name='viagem_solicitacao_list'),
    path('viagem_create/<str:pk>/', ViagemCreate.as_view(), name = 'viagem_create'),
    path('viagem_update/<str:pk>/', ViagemUpdate.as_view(), name='viagem_update'),    
    path('viagem_delete/<int:pk>/',ViagemDelete.as_view(), name='viagem_delete_cbv'),
    path('abastecimento_listall',  AbastecimentoListALL.as_view(), name='abastecimento_listall'),
    path('manutencaoo_listall',  ManutencaoListALL.as_view(), name='manutencao_listall'),
    path('abastecimento_list/<str:pk>/',  AbastecimentoList.as_view(), name='abastecimento_list'),
    path('abastecimento_create/<str:pk>/', AbastecimentoCreate.as_view(), name = 'abastecimento_create'),
    path('abastecimento_update/<str:pk>/', AbastecimentoUpdate.as_view(), name='abastecimento_update'),    
    path('abastecimento_delete/<int:pk>/',AbastecimentoDelete.as_view(), name='abastecimento_delete_cbv'),
    path('veiculo_list',  VeiculoList.as_view(), name='veiculo_list'),
    path('telegram_message', enviar ,name='telegram_message'),
    path('sucesso/', sucesso ,name='sucesso'),
    path('telegram_messageabast', enviarabastecimento ,name='telegram_messageabast'),
    path('retorna_despesas', relatorio_despesa ,name='retorna_despesas'),
    path('retorna_despesascaminhao', relatorio_despesacaminhao ,name='retorna_despesascaminhao'),
    path('retorna_abastecimento_porcaminhao', relatorio_abastecimento_porcaminhao ,name='retorna_abastecimento_porcaminhao'),
    path('retorna_despesastrator', relatorio_despesatrator ,name='retorna_despesastrator'),
    path('retorna_abastecimento_portrator', relatorio_abastecimento_portrator ,name='retorna_abastecimento_portrator'),
    path('retorna_despesasgerador', relatorio_despesagerador ,name='retorna_despesasgerador'),
    path('retorna_abastecimento_porgerador', relatorio_abastecimento_porgerador ,name='retorna_abastecimento_porgerador'),
    path('retorna_abastecimento_porveiculo', relatorio_abastecimento_porveiculo ,name='retorna_abastecimento_porveiculo'),
    path('retorna_manutencao_porveiculo', relatorio_manutencao_porveiculo ,name='retorna_manutencao_porveiculo'),
    path('despesas_frota', IndexDespesas.as_view(), name='despesas_frota'),
    path('manutencao_list/<str:pk>/',  ManutencaoList.as_view(), name='manutencao_list'),
    path('manutencao_create/<str:pk>/', ManutencaoCreate.as_view(), name = 'manutencao_create'),
    path('manutencao_update/<str:pk>/', ManutencaoUpdate.as_view(), name='manutencao_update'),    
    path('manutencao_delete/<int:pk>/',ManutencaoDelete.as_view(), name='manutencao_delete_cbv'),
]
    