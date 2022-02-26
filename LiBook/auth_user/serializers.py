from rest_framework.serializers import ModelSerializer
from app.models import User


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',  'password')  # 'password'
        extra_kwargs = {'password': {'write_only': True}}
