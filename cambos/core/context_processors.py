from core.models import Setor, Periodo

def setores(request):
    return{'setores': Setor.objects.all()}


def get_periodo(request):
    try:
        periodo = Periodo.objects.get(nome = request.GET.get('periodo', None))
    except:
        periodo = Periodo.objects.latest('periodo')
    return {'get_periodo': periodo}


