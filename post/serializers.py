from django.conf import UserSettingsHolder
from django.contrib.auth.models import User
from rest_framework import serializers
from post.models import Post, Comment
from users.serializers import UserSerializer
# from .serializers import CommentRetrieverSerializer

# Serializer to transform a user object into model instance and vice-versa
# class UserSerializer(serializers.ModelSerializer, int):
#     class Meta:
#         model = models.UserProfile
#         fields = '__all__'

# Serializer to transform model instance into readable object
class CommentListRetrieverSerializer(serializers.ModelSerializer):
    createdBy = UserSerializer()
    class Meta:
        model = Comment
        fields = ['id','body', 'createdAt', 'updatedAt', 'createdBy']



# Serializer to transform model instance into readable object
class CommentRetrieverSerializer(serializers.ModelSerializer):
    createdBy = UserSerializer()
    class Meta:
        model = Comment
        fields = ['id','body', 'createdAt', 'post', 'createdBy', 'updatedAt']

class CommentRetrieverForUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']


# Serializer to transform comment object into model instance
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body', 'post' , 'createdBy']


#  Serializer to transform model instance into suitable read format
class PostRetrieveSerializer(serializers.ModelSerializer):
    createdBy = UserSerializer()
    comment_set = CommentListRetrieverSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id','title','body','picture','createdAt','updatedAt','isAnonymous','isSuspended','createdBy','comment_set']


#  Serializer to transform model instance into suitable read format
# class PostRetrieveSerializer(serializers.ModelSerializer):
#     createdBy = UserSerializer()
#     class Meta:
#         model = Post
#         fields = '__all__'


#  Serializer to transform post (python object) into a model instance
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','body','picture','createdBy']
