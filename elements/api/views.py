from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Image
from .serializer import ImageSerializer
from .api import consume_csv_spreadsheet


class ImageCreateView(generics.ListCreateAPIView):
    """
        This view class allows you to:
       - list all de Images from the api: api/image  <GET>
       - create a new Image: api/image {title, description, img} <POST>
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new image."""
        serializer.save()


class ImageDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
        This view class handles the http GET, PUT and DELETE
        requests for an specific image.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class Data(APIView):
    """
       This view allows you to load image data from a spreadsheet
    """
    def get(self, request, format=None):
        try:
            consume_csv_spreadsheet()
            return Response()
        except Exception as e:
            raise e


class ImageListAPIView(generics.ListAPIView):
    """
        This view implements a cache and also allows you to:
       - list all de Images from the api: api/image  <GET>
       - get one specific image by its id: api/image/{:id} <GET>
    """
    serializer_class = ImageSerializer
    queryset = Image.objects.all()

    @method_decorator(cache_page(3600))
    def dispatch(self, *args, **kwargs):
        return super(ImageListAPIView, self).dispatch(*args, **kwargs)
