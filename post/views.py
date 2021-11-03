from users.models import UserProfile
from posuga.permissions import IsUserAuthenticated, IPermissions, permission_denied_error_message
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework import filters
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from post import models
from post import serializers



class PostAPIView(generics.ListCreateAPIView):
    """
    Concrete view for listing and creating post.
    """
    permission_classes = [IsUserAuthenticated]
    serializer_class = serializers.PostSerializer
    queryset = models.Post.objects.filter(isSuspended = False)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body']

    def list(self, request, *args, **kwargs):
        user_permissions = request.user['userpermission']['post']
        if IPermissions.READ.value in user_permissions:
            queryset = self.filter_queryset(models.Post.objects.filter(isSuspended = False))
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = serializers.PostRetrieveSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = serializers.PostRetrieveSerializer(queryset, many=True)
            return Response(request.user)
        return Response({"result": permission_denied_error_message}, status= status.HTTP_401_UNAUTHORIZED)


    def create(self, request, *args, **kwargs):
        user_permissions = request.user['userpermission']['post']
        if IPermissions.CREATE.value in user_permissions:
            serializer = serializers.PostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            serializer_retrieve = serializers.PostRetrieveSerializer(instance)
            headers = self.get_success_headers(serializer_retrieve.data)
            return Response(serializer_retrieve.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"result": permission_denied_error_message}, status= status.HTTP_401_UNAUTHORIZED)

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """
    permission_classes = [IsUserAuthenticated]
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.PostRetrieveSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user_permissions = request.user['userpermission']['post']
        if IPermissions.UPDATE.value in user_permissions:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = serializers.PostSerializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            returned_instance = serializers.PostRetrieveSerializer(instance)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(returned_instance.data)
        return Response({"result": permission_denied_error_message}, status= status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        user_permissions = request.user['userpermission']['post']
        if IPermissions.DELETE.value in user_permissions:
            instance = get_object_or_404(models.Post, pk= kwargs['pk'])
            print(self.request.user['id'], instance.createdBy.id)
            if int(self.request.user['id']) == instance.createdBy.id: #or self.request.user.is_superuser: # delete only when user is the owner of post or admin
                instance.delete()
                return Response({"result":"Deleted successfully"},status= status.HTTP_204_NO_CONTENT)
            return Response({"result":"Unauthorized operation"},status= status.HTTP_401_UNAUTHORIZED)
        return Response({"result": permission_denied_error_message}, status= status.HTTP_401_UNAUTHORIZED)



class CommentListAPIView(generics.ListAPIView):
        """
        Concrete view for reading comments on a post instance.
        """
        permission_classes = [IsUserAuthenticated]
        queryset = models.Comment.objects.all()
        serializer_class = serializers.CommentRetrieverSerializer

        def get_queryset(self):
            a_post = get_object_or_404(models.Post, pk = self.kwargs['post_id'])
            query = models.Comment.objects.filter(post = a_post)
            return query
        
            
class CommentCreateAPIView(generics.CreateAPIView):
    """
    Concrete view for creating comments on a post instance.
    """
    permission_classes = [IsUserAuthenticated]
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def create(self, request, *args, **kwargs):
            serializer = serializers.CommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            serializer_retrieve = serializers.CommentRetrieverSerializer(instance)
            headers = self.get_success_headers(serializer_retrieve.data)
            return Response(serializer_retrieve.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsUserAuthenticated]

    """
    Concrete view for  updating and deleting comments.
    """
    permission_classes = [IsUserAuthenticated]
    serializer_class = serializers.CommentRetrieverForUpdateSerializer

    def get_queryset(self):
        query = models.Comment.objects.filter(pk = self.kwargs['pk'])
        return query
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.CommentRetrieverSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        get_comment_error_response = "Comment not found"
        comment = get_object_or_404(models.Comment, pk = self.kwargs['pk'], createdBy = request.user.id) 
        if comment:
            data = JSONParser().parse(request)
            serializer = serializers.CommentRetrieverForUpdateSerializer(comment, data= data)
            if serializer.is_valid():
                instance = serializer.save()
                retrieved_serializer = serializers.CommentRetrieverSerializer(instance)
                return Response(retrieved_serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response(get_comment_error_response, status= status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        """
        Concrete view delete a comment on a post instance.
        """
        comment = get_object_or_404(models.Comment, pk= kwargs['pk'])
        if int(request.user['id']) == comment.createdBy.id : # or request.user.role ==IsADMIN: #delete only user is owner of comment or admin
            comment.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        return Response(status= status.HTTP_401_UNAUTHORIZED)



class PostByUserAPIView(generics.ListAPIView):
    """
    Concrete view for listing posts created by a specific user.
    """
    permission_classes = [IsUserAuthenticated]
    serializer_class = serializers.PostRetrieveSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body']

    def list(self, request, *args, **kwargs):
        user_permissions = request.user['userpermission']['post']
        if IPermissions.READ.value in user_permissions:
            user = UserProfile.objects.get(pk = kwargs['id'])
            queryset = models.Post.objects.filter(createdBy = user)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = serializers.PostRetrieveSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = serializers.PostRetrieveSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"result": permission_denied_error_message}, status= status.HTTP_401_UNAUTHORIZED)


class SearchPostAPIView(generics.ListAPIView):
    """
    Concrete view for listing posts created by a specific user.
    """
    permission_classes = [IsUserAuthenticated]
    serializer_class = serializers.PostRetrieveSerializer
    queryset = models.Post.objects.all()

    def list(self, request, *args, **kwargs):
        search_text = kwargs['search_text']
        queryset = models.Post.objects.filter(Q(title__icontains=search_text) | Q(body__icontains=search_text))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
