from .models import Med
from .serializers import MedSerializer
from rest_framework import permissions, status, pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

def getCounts(meds):
    currentCount = meds.filter(end_date_num__isnull=True).count()
    oldCount = meds.filter(end_date_num__isnull=False).count()
    return {'currentCount': currentCount, 'oldCount': oldCount}

# Create your views here.
class MedListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        meds = Med.objects.filter(user=self.request.user)
        medprob = request.query_params.get('medprob')
        print(medprob)
        if medprob:
            filter1 = meds.filter(assoc_medprob__icontains='blood pressure')
            filter2 = meds.filter(assoc_medprob__icontains='hypertension')
            meds = filter1 | filter2
            serializer = MedSerializer(meds, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            currentMeds = meds.filter(end_date_num__isnull=True)
            current_serializer = MedSerializer(currentMeds, many=True)
            oldMeds = meds.filter(end_date_num__isnull=False)
            old_serializer = MedSerializer(oldMeds, many=True)
            data = {'current': current_serializer.data} | {'old': old_serializer.data}
            return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = MedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MedDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Med.objects.get(pk=pk)
        except Med.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        med = self.get_object(pk)
        serializer = MedSerializer(med)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        med = self.get_object(pk)
        print(request.data)
        serializer = MedSerializer(med, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        med = self.get_object(pk)
        med.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)