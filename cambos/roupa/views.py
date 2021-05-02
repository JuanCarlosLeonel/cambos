from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import requests
from requests.auth import HTTPBasicAuth

@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'roupa/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = requests.get(
            url='http://ec2-34-212-204-187.us-west-2.compute.amazonaws.com:8000/core/api/users/b9d36a5f-fe64-45fd-929c-280303bb966b/',
            auth=HTTPBasicAuth('admin', 'admin')
        )
        dados = url.json()
        context['dados'] = dados
        return context
