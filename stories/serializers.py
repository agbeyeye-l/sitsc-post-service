from rest_framework import serializers
from stories.models import Story
from users.serializers import UserSerializer


#  Serializer to transform model instance into suitable read format
class StoryRetrieverSerializer(serializers.ModelSerializer):
    createdBy = UserSerializer()
    class Meta:
        model = Story
        fields = '__all__'


#  Serializer to transform stories (python object) into a model instance
class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'