from rest_framework import serializers
from users.models import UserProfile

# Serializer to transform a user object into model instance and vice-versa
class UserSerializer(serializers.ModelSerializer, int):
    class Meta:
        model = UserProfile
        fields = '__all__'