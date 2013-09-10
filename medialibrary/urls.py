from django.conf.urls import patterns, url
from .views import MediaLibraryAPIView, MediaLibraryItemView, AddShelfRelationAPIView

urlpatterns = patterns('',
    url(r'^(?P<type>(audio|video|image))/$', MediaLibraryAPIView.as_view(), name='medialibrary'),
    url(r'^(?P<pk>\d+)/$', MediaLibraryItemView.as_view(), name='medialibrary-shelf'),
    url(r'^(?P<pk>\d+)/add/$', AddShelfRelationAPIView.as_view(), name='medialibrary-shelf-add-relation')
)
