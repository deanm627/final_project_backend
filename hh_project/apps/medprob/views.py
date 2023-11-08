from .models import BP
from .serializers import BPSerializer, BPAvgSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.http import Http404
from django.db.models import Avg, Min
from datetime import date, timedelta, datetime
import calendar

def calcAvg(dataset, date, label):
    if dataset:
        count = dataset.count()
        avg_sys = dataset.aggregate(Avg('systolic'))
        avg_dia = dataset.aggregate(Avg('diastolic'))
        avg_sys = round(avg_sys['systolic__avg'])
        avg_dia = round(avg_dia['diastolic__avg'])
        avg_data = BPAvg(avg_sys, avg_dia, count, date)
    else:
        avg_data = BPAvg(0, 0, 0, date)
    serializer = BPAvgSerializer(avg_data)
    data = {label: serializer.data}
    return data


def avgData(dataset, date):
    dataset_am = dataset.filter(time_num__hour__lt=(12))
    dataset_pm = dataset.filter(time_num__hour__gte=(12))
    data = calcAvg(dataset, date, 'all')
    data_am = calcAvg(dataset_am, date, 'am')
    data_pm = calcAvg(dataset_pm, date, 'pm')
    data = data | data_am | data_pm
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
        first_date = bps.aggregate(Min('date_num'))
        date = first_date['date_num__min']
        num = request.query_params.get('num')
        interval = request.query_params.get('type')
        
        if num:
            num = int(num)
            match interval:
                case 'year':
                    num_days = num * 365
                case 'month':
                    num_days = num * 30
                case 'week':
                    num_days = num * 7
                case _:
                    num_days = num
            print('NUM_DAYS: ', num_days)
            if (num_days > 365 and interval == 'year'):
                num_years = int(num_days/365)
                year = date.today().year
                data_chart = {}
                while num_years > 0:
                    year_data = bps.filter(date_num__year=year)
                    data_chart = data_chart | calcAvg(year_data, date, year)
                    year -= 1
                    num_years -= 1
                data_chart = {'data_chart': data_chart}

            elif (num_days > 30 and interval == 'month'):
                num_months = int(num_days/30)
                month = date.today().month
                data_chart = {}
                while num_months > 0:
                    if (month == 0):
                        month = 12
                    month_data = bps.filter(date_num__month=month)
                    print(calendar.month_name[month])
                    print(month_data)
                    data_chart = data_chart | calcAvg(month_data, date, calendar.month_abbr[month])
                    month -= 1
                    num_months -= 1
                data_chart = {'data_chart': data_chart}
            
            elif ((num_days > 7 and interval == 'week') or (num == 1 and interval == 'month')):
                num_weeks = int(num_days/7)
                data_chart = {}
                start = date.today()
                while num_weeks > 0:
                    end = start - timedelta(days=6)
                    print("START: ", start)
                    print("END: ", end)
                    week_data = bps.filter(date_num__range=[end, start])
                    print(week_data)
                    data_chart = data_chart | calcAvg(week_data, end, f'Week {num_weeks}')
                    print(data_chart)
                    start = start - timedelta(days=7)
                    num_weeks -= 1
                data_chart = {'data_chart': data_chart}
            
            else: 
                days = num
                data_chart = {}
                start = date.today()
                while days > 0:
                    day_data = bps.filter(date_num=start)
                    print("START: ", start)
                    print(day_data)
                    data_chart = data_chart | calcAvg(day_data, start, f'Day {days}')
                    print(data_chart)
                    start = start - timedelta(days=1)
                    days -= 1
                data_chart = {'data_chart': data_chart}

            startdate = date.today()
            enddate = startdate - timedelta(days=num_days)
            bps = bps.filter(date_num__range=[enddate, startdate])
            date = enddate
            data = avgData(bps, date) | data_chart
            return Response(data)
        else:
            data = avgData(bps, date)
            return Response(data)

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