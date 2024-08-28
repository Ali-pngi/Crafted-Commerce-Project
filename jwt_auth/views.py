from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .common import UserSerializer
from utils.decorators import handle_exceptions

User = get_user_model()

# SignUp View
class SignUpView(APIView):

    # Create user
    @handle_exceptions
    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response({ 'message': 'Sign up successful.'}, 201)
        return Response(user_to_create.errors, 400)
    

# SignIn View
class SignInView(APIView):

    @handle_exceptions
    def post(self, request):
        # Extract username and password from the request
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Sign in successful.'
            }, 200)
        else:
            return Response({'error': 'Invalid credentials.'}, 401)