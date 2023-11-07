from .models import BP
from .serializers import BPSerializer, BPAvgSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.http import Http404
from django.db.models import Avg, Min
from datetime import date, timedelta, datetime

def calcAvg(dataset, date):
    count = dataset.count()
    avg_sys = dataset.aggregate(Avg('systolic'))
    avg_dia = dataset.aggregate(Avg('diastolic'))
    avg_sys = round(avg_sys['systolic__avg'])
    avg_dia = round(avg_dia['diastolic__avg'])
    data = BPAvg(avg_sys, avg_dia, count, date)
    return data

class BPAvg:
    def __init__(self, sys_avg, dia_avg, count, first_date):
        self.sys_avg = sys_avg
        self.dia_avg = dia_avg
        self.count = count
        self.first_date = first_date

class BPSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        bps = BP.objects.filter(user=self.request.user)
        timetest1 = bps.filter(time_num__hour__lt=(12))
        print('TIMETEST1:', timetest1)
        timetest2 = bps.filter(time_num__hour__gte=(12))
        print('TIMETEST2:', timetest2)
        first_date = bps.aggregate(Min('date_num'))
        date = first_date['date_num__min']
        num_days = request.query_params.get('days')
        print(num_days)
        if num_days:
            num_days = int(num_days)
            startdate = date.today()
            enddate = startdate - timedelta(days=num_days)
            print(enddate, startdate)
            print(bps)
            print(bps.count())
            bps = bps.filter(date_num__range=[enddate, startdate])
            print(bps)
            print(bps.count())
            date = enddate
        data = calcAvg(bps, date)
        serializer = BPAvgSerializer(data)
        obj = {'generic': serializer.data}
        print(obj)
        print(serializer.data)
        return Response(serializer.data)

class BPListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        bps = BP.objects.filter(user=self.request.user)
        date1 = request.query_params.get('date1')
        date2 = request.query_params.get('date2')
        if date1:
            if (date1 > date2):
                bps = bps.filter(date_num__range=[date2, date1])
            elif (date2 > date1):
                bps = bps.filter(date_num__range=[date1, date2])
            else:
                bps = bps.filter(date_num=date1)
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
        print(serializer.data)
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