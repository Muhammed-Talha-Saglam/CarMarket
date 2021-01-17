from django.db import models


class Car(models.Model):

    date = models.DateField()
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.FloatField()
    color = models.CharField(max_length=50)
    km = models.FloatField()
    price = models.FloatField()
