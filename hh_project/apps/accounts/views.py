from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer, NewUserSerializer
from django.contrib.auth.hashers import make_password
from django.http import Http404

# Create your views here.
class LoginView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = CustomUser.objects.get(username = self.request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def get(self, request):
        userInfo = CustomUser.objects.get(username = self.request.user)
        serializer = UserSerializer(userInfo)
        return Response(serializer.data)

    def post(self, request):
        if CustomUser.objects.filter(email__iexact=request.data['email']).exists():
            content = 'There is already an account with this email.'
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif CustomUser.objects.filter(username__iexact=request.data['username']).exists():
            content = 'Username already exists, please choose another'
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = NewUserSerializer(data=request.data)
            if serializer.is_valid():
                new_user = serializer.save()
                new_user.password = make_password(request.data['password'])
                new_user.save()
                return Response('Success', status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        print(request.data)
        setWithoutUser = CustomUser.objects.exclude(pk=pk)
        print(setWithoutUser)
        if setWithoutUser.filter(email__iexact=request.data['email']).exists():
            content = 'There is already an account with this email.'
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif setWithoutUser.filter(username__iexact=request.data['username']).exists():
            content = 'Username already exists, please choose another'
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = self.get_object(pk)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)