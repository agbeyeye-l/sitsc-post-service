from users.models import UserProfile
from rest_framework import status
from rest_framework import filters
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import generics
from gallery.models import Gallery
from gallery.serializers import GalleryPostSerializer, GalleryRetrieveSerializer
from posuga.permissions import IsUserAuthenticated,IPermissions,permission_denied_error_message

# Default response messages
operation_success_message = "Operation successful"
operation_unauthorized_message = "Unauthorized operation"


class GalleryCreateList(generics.ListCreateAPIView):
    """
    Concrete view for creating and listing photos/images.
    """
    permission_classes = [IsUserAuthenticated]
    serializer_class  = GalleryRetrieveSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tag']

    def list(self, request, *args, **kwargs):
        user_permissions = request.user['userpermission']['gallery']
        if IPermissions.READ.value in user_permissions:
            try:
                queryset = self.filter_queryset(Gallery.objects.all())
            except:
                queryset = Gallery.objects.all()

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = GalleryRetrieveSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = GalleryRetrieveSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"result": permission_denied_error_message}, status= status.HTTP_401_UNAUTHORIZED)
    
    def create(self, request, *args, **kwargs):
        user_permissions = request.user['userpermission']['gallery']
        if IPermissions.CREATE.value in user_permissions:
            serializer = GalleryPostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            serializer_retrieve = GalleryRetrieveSerializer(instance)
            headers = self.get_success_headers(serializer_retrieve.data)
            return Response(serializer_retrieve.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"result": permission_denied_error_message}, status= status.HTTP_401_UNAUTHORIZED)
    

class GalleryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Concrete view for retrieving and deleting a photo/image.
    """
    permission_classes = [IsUserAuthenticated]
    queryset = Gallery.objects.all()
    serializer_class  = GalleryRetrieveSerializer

    # update a gallery
    def update(self, request, *args, **kwargs):
        user_permissions = request.user['userpermission']['gallery']
        if IPermissions.UPDATE.value in user_permissions:
            get_comment_error_response = "Gallery not found"
            gallery = get_object_or_404(Gallery, pk = self.kwargs['pk'], createdBy = request.user['id']) 
            if gallery:
                data = JSONParser().parse(request)
                serializer = GalleryPostSerializer(gallery, data= data)
                if serializer.is_valid():
                    instance = serializer.save()
                    retrieved_serializer = GalleryRetrieveSerializer(instance)
                    return Response(retrieved_serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response({"result": get_comment_error_response}, status= status.HTTP_404_NOT_FOUND)
        return Response({"result": permission_denied_error_message}, status= status.HTTP_401_UNAUTHORIZED)

    # delete a photo in the gallery
    def destroy(self, request, *args, **kwargs):
        user_permissions = request.user['userpermission']['gallery']
        if IPermissions.DELETE.value in user_permissions:
            instance = get_object_or_404(Gallery, pk=kwargs['pk'])
            if int(self.request.user['id']) == instance.createdBy.id: # or self.request.user.role == IsADMIN:  # if the user is the owner of the photo or the admin
                instance.delete()
                return Response({"result": operation_success_message},status= status.HTTP_204_NO_CONTENT)
            return Response({"result": operation_unauthorized_message},status= status.HTTP_401_UNAUTHORIZED)
        return Response({"result": permission_denied_error_message}, status= status.HTTP_401_UNAUTHORIZED)


class GalleryByUserAPIView(generics.ListAPIView):
    """
    Concrete view for creating and listing photos/images uploaded by a particular user.
    """
    permission_classes = [IsUserAuthenticated]
    serializer_class  = GalleryRetrieveSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tag']

    def list(self, request, *args, **kwargs):
        user_permissions = request.user['userpermission']['gallery']
        if IPermissions.READ.value in user_permissions:
            target_user = get_object_or_404(UserProfile, pk=kwargs['user_id'])
            queryset = self.filter_queryset(Gallery.objects.filter(createdBy = target_user))
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = GalleryRetrieveSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = GalleryRetrieveSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"result": permission_denied_error_message}, status= status.HTTP_401_UNAUTHORIZED)
