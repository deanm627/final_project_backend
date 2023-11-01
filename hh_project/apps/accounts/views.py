from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer, NewUserSerializer
from django.contrib.auth.hashers import make_password

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
    def post(self, request):
        print(request.data)
        print(request.data['username'])
        try:
            CustomUser.objects.get(username__iexact=request.data['username'])
            return Response('username already exists', status=status.HTTP_400_BAD_REQUEST)
        except: 
            serializer = NewUserSerializer(data=request.data)
            if serializer.is_valid():
                new_user = serializer.save()
                new_user.password = make_password(request.data['password'])
                new_user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)