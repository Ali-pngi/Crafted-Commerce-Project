from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['profile_image'] = user.profile_image
        return token
