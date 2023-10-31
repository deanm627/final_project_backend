from rest_framework import serializers 
from .models import BP

class BPSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = BP
        fields = ['systolic', 'diastolic', 'date', 'time', 'user']