from core.models import Setor, Periodo

def setores(request):
    return{'setores': Setor.objects.all()}


def get_periodo(request):
    ultimo_periodo = Periodo.objects.latest('periodo')
    try:
        periodo = Periodo.objects.get(nome = request.GET.get('periodo', None))
    except:
        periodo = ultimo_periodo
    return {'get_periodo': periodo, 'ultimo_periodo': ultimo_periodo.nome}


