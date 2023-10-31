from django.shortcuts import render
from .models import BP
from .serializers import BPSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions

# Create your views here.
class BPViewSet(viewsets.ModelViewSet):
    queryset = BP.objects.all()
    serializer_class = BPSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)