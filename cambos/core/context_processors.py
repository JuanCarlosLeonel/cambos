from core.models import Setor

def setores(request):
    return{'setores': Setor.objects.all()}
