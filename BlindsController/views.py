from BlindsController.models import Window
from BlindsController.serializers import WindowSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
import sys
import time
from gattlib import GATTRequester, GATTResponse


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

received = False
dataReceived = ""
class Requester(GATTRequester):
    def on_notification(self, handle, data):
        global received
	global dataReceived
        received = True
	dataReceived = data
	self.disconnect()

def sendSteps(address, handle, steps, turnTime=5, timeout=9):
    global received
    delay = 0.25
    try:
        requester = Requester(address)
        t = 0.0
        time.sleep(delay)
        while not requester.is_connected() and t < timeout:
                print(t)
                t += delay
                time.sleep(delay)
        requester.write_by_handle(handle, " " + steps)
    except Exception as ex:
        print(ex)
        return {"steps":-999, "battery":-999}
        
    response = GATTResponse()
    requester.read_by_handle_async(handle, response)
    while not received:
        time.sleep(0.1)
    while requester.is_connected() and t < timeout:
        t += delay
        time.sleep(delay)
        requester.disconnect()
    print("DataReceived: " + dataReceived)
    battery=dataReceived.split(":")[1].split("\n")[0]
    print("Battery: " + battery) 
    received = False
    return {"steps":steps, "battery":int(battery)}


@api_view(['GET'])
def tiltwindow(request, pk, format=None):
    turnedsteps=0;
    queryset = Window.objects.all()
    serializer_class = WindowSerializer

    try:
        window = Window.objects.get(pk=pk)
    except Window.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if window.turning:
        return Response({"message":"Motor already turning"}, status=status.HTTP_400_BAD_REQUEST)

    window.turning = True
    window.save
    serializedWindow = WindowSerializer(window)
    serializer = WindowSerializer(window, serializedWindow.data)
    serializer.save

    newangle = int(float(request.query_params.get('targetangle', -999.0)))
    motorDelay = int(request.query_params.get('sleep', 5))
    timeout = int(request.query_params.get('timeout', 9));
    if newangle == -999:
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

    if steps != 0:
 	steps = int(steps)
        turnedsteps = -999
	result = sendSteps(str(window.address), window.handle, str(steps), motorDelay, timeout)
        print("Here I am")
	turnedsteps=result["steps"]
    if (turnedsteps != 0) and (turnedsteps != -999):
    	window.currentangle = newangle
    	window.stepsfromzero = steps + window.stepsfromzero
	window.batterylevel = result["battery"]
    window.turning = False
    window.save
    serializedWindow = WindowSerializer(window)
    serializer = WindowSerializer(window, serializedWindow.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"window":serializer.data, "steps":steps})
    else:
        return Response(serializer.errors)

