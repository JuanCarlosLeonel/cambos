from django.forms import ModelForm
from .models import Etapa


class EtapaForm(ModelForm):
        class Meta:
            model = Etapa
            fields = ['processo', 'calendario', 'nome', 'interno', 'capacidade', 'linha', 'tag', 'nick_spi']