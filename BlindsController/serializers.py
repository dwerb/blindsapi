from rest_framework import serializers
from BlindsController.models import Window

class WindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Window
        fields = ('id', 'name', 'address', 'currentangle', 'turning', 'stepsfromzero', 'tiltupsteps', 'tiltdownsteps', 'batterylevel')
