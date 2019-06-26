from django.urls import include, path
from django.contrib import admin

from ui_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('config/', include('config_management.urls', namespace='config_management')),
    path('', views.home),
]
