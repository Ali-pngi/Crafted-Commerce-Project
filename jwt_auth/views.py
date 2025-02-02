from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .serializers import UserSerializer, CustomObtainPairSerializer
from .models import User  
from rest_framework.decorators import api_view
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

logger = logging.getLogger(__name__)


class SignUpView(APIView):
    def post(self, request):
        logger.info(f"Received signup request with data: {request.data}")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'date_joined': user.date_joined.isoformat(),
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            logger.info(f"User created successfully: {user.username}")
            return Response(response_data, status=status.HTTP_201_CREATED)
        logger.error(f"Validation errors: {serializer.errors}")
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
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if int(user_id) != request.user.id:
            return Response({"error": "You can only view your own profile"}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, user_id):
        if int(user_id) != request.user.id:
            return Response({"error": "You can only update your own profile"}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

