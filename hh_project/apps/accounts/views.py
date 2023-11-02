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
        if CustomUser.objects.filter(username__iexact=request.data['username']).exists():
            reason = 'Username already exists, please choose another'
            return Response(reason, status=status.HTTP_400_BAD_REQUEST)
        elif CustomUser.objects.filter(email__iexact=request.data['email']).exists():
            reason = 'There is already an account with this email.'
            return Response(reason, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = NewUserSerializer(data=request.data)
            if serializer.is_valid():
                new_user = serializer.save()
                new_user.password = make_password(request.data['password'])
                new_user.save()
                return Response('Success', status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)