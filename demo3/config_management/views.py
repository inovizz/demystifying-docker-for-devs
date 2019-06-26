from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from config_management.models import Config

class ConfigList(ListView):
    model = Config

class ConfigCreate(CreateView):
    model = Config
    fields = ['name', 'value']
    success_url = reverse_lazy('config_management:config_list')

class ConfigEdit(UpdateView):
    model = Config
    fields = ['name', 'value']
    success_url = reverse_lazy('config_management:config_list')

class ConfigDelete(DeleteView):
    model = Config
    success_url = reverse_lazy('config_management:config_list')