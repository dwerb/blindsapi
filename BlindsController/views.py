from BlindsController.models import Window
from BlindsController.serializers import WindowSerializer
from rest_framework import generics
from rest_framework.response import Response


class WindowList(generics.ListCreateAPIView):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer


class WindowDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer

    def update(self, request, pk):
        try:
            window = Window.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        print(request.data)
        serializer = WindowSerializer(window, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
