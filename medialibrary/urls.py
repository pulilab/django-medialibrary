from django.conf.urls import patterns, url
from .views import MediaLibraryAPIView

urlpatterns = patterns('',
    url(r'^(?P<type>(audio|video|image))/$', MediaLibraryAPIView.as_view(), name='medialibrary'),
)
