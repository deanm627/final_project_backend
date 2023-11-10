from .models import Med
from .serializers import MedSerializer
from rest_framework import permissions, status, pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

# Create your views here.
class MedListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        meds = Med.objects.filter(user=self.request.user)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(meds, request)
        serializer = MedSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        print(request.data)
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
        return Response(serializer.data)
    
    def put(self, request, pk):
        med = self.get_object(pk)
        print(request.data)
        serializer = MedSerializer(med, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        med = self.get_object(pk)
        med.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)