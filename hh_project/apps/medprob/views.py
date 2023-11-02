from django.shortcuts import render
from .models import BP
from .serializers import BPSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.http import Http404
from django.db.models import Avg, Min

class BPSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        bps = BP.objects.filter(user=self.request.user)
        count = {'count': bps.count()}
        avg_sys = bps.aggregate(Avg('systolic'))
        avg_dia = bps.aggregate(Avg('diastolic'))
        first_date = bps.aggregate(Min('date'))
        # serializer_sys = BPSerializer(avg_sys)
        # serializer_dia = BPSerializer(avg_dia)
        print(avg_sys)
        print(avg_dia)
        print(count)
        print(first_date)
        data = avg_sys | avg_dia | count | first_date
        print(data)
        # content = serializer_sys.data + serializer_dia.data
        # print(content)
        return Response(data)

class BPListView(APIView):
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
    
class BPDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return BP.objects.get(pk=pk)
        except BP.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        bp = self.get_object(pk)
        serializer = BPSerializer(bp)
        return Response(serializer.data)
    
    def put(self, request, pk):
        bp = self.get_object(pk)
        serializer = BPSerializer(bp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        bp = self.get_object(pk)
        bp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)