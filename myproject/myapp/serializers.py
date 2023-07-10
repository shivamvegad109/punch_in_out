from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

class PunchinSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()