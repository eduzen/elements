import base64

from django.core.files import File
from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    image_compress_base64 = serializers.SerializerMethodField()
    image_compress_url = serializers.SerializerMethodField()

    def get_image_compress_base64(self, obj):
        with open(obj.image_compress.path, 'rb') as file:
            image = File(file)
            data = base64.b64encode(image.read())
        return data

    def get_image_compress_url(self, obj):
        request = self.context.get('request')
        image_compress_url = obj.image_compress.url
        return request.build_absolute_uri(image_compress_url)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Image
        fields = ('id', 'title', 'description', 'upload_date',
                  'image_original', 'image_compress_url', 'image_compress_base64', )
