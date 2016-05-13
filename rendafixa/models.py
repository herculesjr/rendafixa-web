from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Issuer(models.Model):


class BoundType(models.Model):

class Bound(models.Model):
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE)
    bound_type = models.ForeignKey(BoundType, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    identifier = models.CharField(max_length=100)
    expiration_date = models.DateTimeField('Expiration date')
    term_days = models.BigIntegerField()
    last_buy_price = models.DecimalField()
    last_buy_tax = models.DecimalField()
    last_sell_price = models.DecimalField()
    last_sell_tax = models.DecimalField()
    last_update = models.DateTimeField('Last Update')

class BoundData(models.Model):
    bound = models.ForeignKey(Bound, on_delete=models.CASCADE)
    buy_price = models.DecimalField()
    buy_tax = models.DecimalField()
    sell_price = models.DecimalField()
    sell_tax = models.DecimalField()
