from django.db import models

class CatDog(models.Model):
    animal = models.CharField(max_length=100)
    path = models.TextField()
