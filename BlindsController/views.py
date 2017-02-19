from BlindsController.models import Window
from BlindsController.serializers import WindowSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json


class WindowList(generics.ListCreateAPIView):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer


class WindowDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer

    def update(self, request, pk):
        try:
            window = Window.objects.get(pk=pk)
        except Window.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        print(request.data)
        serializer = WindowSerializer(window, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def tiltwindow(request, pk):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer

    try:
        window = Window.objects.get(pk=pk)
    except Window.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    newangle = int(request.query_params.get('targetangle', None))
    if newangle is None:
        return Response({"message": "Invalid parameter. Expecting targetangle"})
    elif (newangle < -90) or (newangle > 90):
        return Response({"message": "TargetAngle must be between -90 and 90 degrees"})
    elif newangle == -90:
        steps = window.tiltupsteps - window.stepsfromzero
    elif newangle == 90:
        steps = window.tiltdownsteps - window.stepsfromzero
    elif newangle == 0:
        steps = 0 - window.stepsfromzero
    elif newangle < 0:
        stepsPerAngle = window.tiltupsteps / -90.0
        steps = (stepsPerAngle*newangle) - window.stepsfromzero
    elif newangle > 0:
        stepsPerAngle = window.tiltdownsteps / 90.0
        steps = (stepsPerAngle*newangle) - window.stepsfromzero
    else:
        return Response({"message": "Got some data!", "targetangle": newangle, "currentangle":window.currentangle})

#turn motor
    window.currentangle = newangle
    window.stepsfromzero = steps + window.stepsfromzero
    window.save
    serializedWindow = WindowSerializer(window)
    serializer = WindowSerializer(window, serializedWindow.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"window":serializer.data, "steps":steps})
    else:
        return Response(serializer.errors)

