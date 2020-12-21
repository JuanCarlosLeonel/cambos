from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'core/index.html'


@method_decorator(login_required, name='dispatch')
class TextilP(TemplateView):
    template_name = 'core/textilp.html'