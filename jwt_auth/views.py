# jwt_auth/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from django.contrib.auth.models import User

class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view

@api_view(['GET'])
def check_username(request):
    username = request.query_params.get('username', None)
    if not username:
        return Response({'error': 'Username parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'available': False}, status=status.HTTP_200_OK)
    else:
        return Response({'available': True}, status=status.HTTP_200_OK)

@api_view(['GET'])
def check_email(request):
    email = request.query_params.get('email', None)
    if not email:
        return Response({'error': 'Email parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({'available': False}, status=status.HTTP_200_OK)
    else:
        return Response({'available': True}, status=status.HTTP_200_OK)


