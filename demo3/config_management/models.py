from django.db import models
from django.urls import reverse


class Config(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('config_management:config_form', kwargs={'pk': self.pk})