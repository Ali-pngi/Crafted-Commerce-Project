from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from .common import UserSerializer
from utils.decorators import handle_exceptions

User = get_user_model()

class SignUpView(APIView):

    @handle_exceptions
    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            user = user_to_create.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Sign up successful.'
            }, status=201)
        else:
            return Response(user_to_create.errors, status=400)

class SignInView(APIView):
    @handle_exceptions
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"Received username: {username}, password: {password}")
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Sign in successful.'
            }, status=200)
        else:
            return Response({'error': 'Invalid credentials.'}, status=401)

@api_view(['GET'])
def check_username(request):
    username = request.query_params.get('username', None)
    if username:
        exists = User.objects.filter(username=username).exists()
        return Response({'available': not exists}, status=200)
    return Response({'error': 'Username parameter not provided.'}, status=400)

@api_view(['GET'])
def check_email(request):
    email = request.query_params.get('email', None)
    if email:
        exists = User.objects.filter(email=email).exists()
        return Response({'available': not exists}, status=200)
    return Response({'error': 'Email parameter not provided.'}, status=400)
