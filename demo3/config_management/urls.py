from django.urls import path

from . import views

app_name = 'books_cbv'

urlpatterns = [
  path('', views.ConfigList.as_view(), name='config_list'),
  path('create', views.ConfigCreate.as_view(), name='config_create'),
  path('edit/<int:pk>', views.ConfigEdit.as_view(), name='config_form'),
  path('delete/<int:pk>', views.ConfigDelete.as_view(), name='config_delete'),
]