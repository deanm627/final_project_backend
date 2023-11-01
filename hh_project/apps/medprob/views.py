from django.shortcuts import render
from .models import BP
from .serializers import BPSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

# Create your views here.
# class BPViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = BP.objects.all()
#     serializer_class = BPSerializer
    
#     @action(detail=False, methods=['GET'])
#     def print_user(self, request):
#         print('hellooooo')
#         print(self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

class BPView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        bps = BP.objects.filter(user=self.request.user)
        serializer = BPSerializer(bps, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        print(request.data)
        serializer = BPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)