from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .serializers import UserSerializer, CustomObtainPairSerializer
from .models import User  
from rest_framework.decorators import api_view

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

class SignInView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.user
        response_data = serializer.validated_data
        response_data['user_id'] = user.id
        response_data['username'] = user.username
        response_data['email'] = user.email
        response_data['is_superuser'] = user.is_superuser
        response_data['date_joined'] = user.date_joined.isoformat()
        
        return Response(response_data, status=status.HTTP_200_OK)

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