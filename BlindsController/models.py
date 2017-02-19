from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Window(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    address = models.CharField(max_length=30, blank=False, default='')
    currentangle = models.IntegerField(default=0)
    stepsfromzero = models.IntegerField(default=0)
    tiltupsteps = models.IntegerField(default=0)
    tiltdownsteps = models.IntegerField(default=0)
    batterylevel = models.IntegerField(default=100)
    
    class Meta:
        ordering = ('name', 'address', 'currentangle')
