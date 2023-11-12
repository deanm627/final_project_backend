from rest_framework import serializers 
from .models import Med

class MedSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    start_date_str = serializers.DateField(format="%b %d, %Y")
    end_date_str = serializers.DateField(format="%b %d, %Y", required=False, allow_null=True)
    
    class Meta:
        model = Med
        fields = '__all__'