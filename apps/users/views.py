from django.shortcuts import render
from rest_framework import generics
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .services import LoginService
from rest_framework.response import Response
# Create your views here.

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CustomUser.objects.create_user(
            email = serializer.validated_data['email'],
            password = serializer.validated_data['password']
        )

        return Response({"status": "User created!"})
    
class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    service = LoginService()

    def post(self, request, *args, **kwargs):
        user = self.service.find_user(request)
        self.service.check_user(request, user)
        access, refresh = self.service.give_token(user)
        return Response({'access_token': str(access), 'refresh_token': str(refresh)})
    
