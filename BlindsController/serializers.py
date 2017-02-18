from rest_framework import serializers
from BlindsController.models import Window

class WindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Window
        fields = ('id', 'name', 'address', 'currentposition', 'tiltupsteps', 'tiltdownsteps', 'batterylevel')
