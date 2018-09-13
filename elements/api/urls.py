from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^image/$', views.ImageCreateView.as_view(), name="image_create"),
    url(r'^image/(?P<pk>[0-9]+)/$', views.ImageDetailsView.as_view(), name="image_details"),
    url(r'^cache/image/$', views.ImageListAPIView.as_view(), name="image"),
    url(r'^load_data/$', views.Data.as_view(), name="data"),

]
