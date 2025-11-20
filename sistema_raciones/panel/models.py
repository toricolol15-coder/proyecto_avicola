from django.db import models

class Racion(models.Model):
    nombre = models.CharField(max_length=100)
