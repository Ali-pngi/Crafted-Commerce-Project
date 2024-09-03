from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.pop('password_confirmation', None)

        if password != password_confirmation:
            raise serializers.ValidationError({'password_confirmation': 'Passwords do not match.'})

        try:
            password_validation.validate_password(password=password)
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        data['password'] = make_password(password)
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation', None)
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirmation')


class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate

        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            from rest_framework_simplejwt.tokens import RefreshToken

            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        else:
            raise serializers.ValidationError('Invalid credentials provided.')

    class Meta:
        fields = ('username', 'password', 'access', 'refresh')
