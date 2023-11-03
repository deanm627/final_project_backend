from rest_framework import serializers 
from .models import BP

class BPSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    date = serializers.DateField(format="%b %d, %Y")
    time = serializers.TimeField(format="%I: %M %p")
    
    class Meta:
        model = BP
        fields = ['systolic', 'diastolic', 'date', 'time', 'user', 'id']

class BPDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = BP
        fields = ['systolic', 'diastolic', 'date', 'time', 'user', 'id']

class BPAvgSerializer(serializers.Serializer):
    sys_avg = serializers.IntegerField()
    dia_avg = serializers.IntegerField()
    count = serializers.IntegerField()
    first_date = serializers.DateField(format="%b %d, %Y")