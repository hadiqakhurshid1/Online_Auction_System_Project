from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from time import time

from django.core.validators import *

# Create your models here.
from django.template.context_processors import request

def getImage(instance, filename):
    return "auction_system/image_{0}_{1}".format(str(time()),filename)


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=getImage)
    category = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    minimum_price = models.IntegerField(null=True)
    bid_end_date = models.DateField(default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.id


class Seller(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_name = models.ForeignKey(User)
    product_id = models.ForeignKey(Product)

    def __unicode__(self):
        return unicode(self.user_name)

class Bidder(models.Model):
    numeric = RegexValidator(r'^[0-9]*$', 'Only numerics are allowed.')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_name = models.ForeignKey(User)
    product_id = models.ForeignKey(Product)
    bid_amount = models.CharField(max_length=255, validators=[numeric])

    def __unicode__(self):
        return unicode(self.user_name)

