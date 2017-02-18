from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Window(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    address = models.CharField(max_length=30, blank=False, default='')
    position = models.IntegerField(default=0)
    batterylevel = models.IntegerField(default=100)
    
    class Meta:
        ordering = ('name', 'address', 'position')
