from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from stories.models import Story
from stories.serializers import StoryRetrieverSerializer, StorySerializer
from posuga.permissions import IsUserAuthenticated

class StoryList(APIView):
    """
    Concrete view for listing and creating story.
    """
    permission_classes = [IsUserAuthenticated]
    def get(self, request):
        """
        Concrete view for listing stories.
        """
        stories =  Story.objects.all()
        serializer = StoryRetrieverSerializer(stories, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)

    def post(self, request):
        """
        Concrete view for creating a story.
        """
        data = JSONParser().parse(request)
        serializer = StorySerializer(data = data)
        if serializer.is_valid():
            instance = serializer.save()
            retrieved_instance = StoryRetrieverSerializer(instance)
            return Response(retrieved_instance.data, status= status.HTTP_201_CREATED)
        return Response( serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class StoryDetail(APIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """
    permission_classes = [IsUserAuthenticated]

    # read a single story
    def get(self, request, pk):
        post =  get_object_or_404(Story, pk= pk)
        serializer = StoryRetrieverSerializer(post)
        return Response(serializer.data, status= status.HTTP_200_OK) 

    # Update a story
    def put(self, request, pk):
        data = JSONParser().parse(request)
        instance = get_object_or_404(Story, pk= pk)
        if request.user.id == instance.createdBy.id:
            serializer = StorySerializer(instance= instance, data= data)
            if serializer.is_valid():
                saved_instance = serializer.save()
                retrieved_serializer = StoryRetrieverSerializer(saved_instance)
                return Response(retrieved_serializer.data, status= status.HTTP_200_OK)
            return Response( serializer.errors, status= status.HTTP_400_BAD_REQUEST)    
        return Response(status = status.HTTP_401_UNAUTHORIZED)

    # Delete a post
    def delete(self, request, pk):
        instance = get_object_or_404(Story, pk= pk)
        if int(request.user['id']) == instance.createdBy.id: # or request.user.role ==IsADMIN: # delete only when user is the owner of post or admin
            instance.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        return Response(status= status.HTTP_401_UNAUTHORIZED)


