from django.db import models
from django.urls import reverse_lazy


class Post(models.Model):

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False)
        
    mail = models.CharField(
        max_length=255,
        blank=False,
        null=False)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse_lazy("detail", args=[self.id])
