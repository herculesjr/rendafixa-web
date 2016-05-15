from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.


@python_2_unicode_compatible
class Issuer(models.Model):
    name = models.CharField(max_length=200)
    identifier = models.CharField(max_length=100, unique=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BoundType(models.Model):
    name = models.CharField(max_length=200)
    identifier = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.identifier


@python_2_unicode_compatible
class Bound(models.Model):
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE)
    bound_type = models.ForeignKey(BoundType, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    crawler_name = models.CharField(max_length=200, default='')
    identifier = models.CharField(max_length=100, unique=True)
    expiration_date = models.DateTimeField('Expiration date')
    term_days = models.BigIntegerField(default=0)
    last_update = models.DateTimeField('Last update', auto_now=True)

    def __str__(self):
        return '%s %s (%s)' % (self.name, self.expiration_date.strftime('%Y'), self.bound_type.name)


@python_2_unicode_compatible
class BoundData(models.Model):
    bound = models.ForeignKey(Bound, on_delete=models.CASCADE)
    buy_price = models.DecimalField(decimal_places=2, max_digits=10)
    buy_tax = models.DecimalField(decimal_places=2, max_digits=10)
    sell_price = models.DecimalField(decimal_places=2, max_digits=10)
    sell_tax = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField()

    def __str__(self):
        return '%s %s' % (self.bound, self.date)
