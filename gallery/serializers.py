from rest_framework import serializers
from gallery.models import Gallery
from users.serializers import UserSerializer


class GalleryRetrieveSerializer(serializers.ModelSerializer):
    createdBy = UserSerializer()

    class Meta:
        model = Gallery
        fields = ['id', 'tag', 'images', 'createdAt', 'createdBy', 'updatedAt']


class GalleryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['tag', 'images', 'createdBy']
