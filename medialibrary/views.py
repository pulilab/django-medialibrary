from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Shelf
from .serializers import ShelfSerializer


class MediaLibraryItemView(generics.RetrieveAPIView):
    model = Shelf
    # TODO: should be allowed only for the owner
    permission_classes = (permissions.IsAuthenticated,) 


class MediaLibraryAPIView(generics.ListCreateAPIView):
    """Retrieves and creates shelves of a given type from the MediaLibrary"""
    model = Shelf
    serializer_class = ShelfSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        self.shelf_type = kwargs.get('type')
        return super(MediaLibraryAPIView, self).get(request, *args, **kwargs)

    def get_serializer_context(self):
        ctx = super(MediaLibraryAPIView, self).get_serializer_context()
        ctx['shelf_type'] = self.shelf_type
        ctx['method'] = self.request.method
        return ctx

    def post(self, request, *args, **kwargs):
        self.shelf_type = kwargs.get('type')
        request.DATA['library'] = self.request.user.medialibrary.pk
        request.DATA['name'] = request.FILES.values()[0].name

        # Forbid using this method to upload videofiles, use old /v2/api/upload
        # till it's not refactored.
        # TODO: refactor and remove /v2/api/upload
        if self.shelf_type == 'video':
            return Response({'error': 'not implemented yet, use old videouploader'},
                            status=status.HTTP_403_FORBIDDEN)

        resp = super(MediaLibraryAPIView, self).post(request, *args, **kwargs)

        new_id = resp.data['url'].split('/')[-2]
        new_shelve = self.get_queryset().get(pk=new_id)
        context = self.get_serializer_context()
        context['method'] = 'GET'
        resp_serializer = self.serializer_class(new_shelve, context=context)
        resp.data = resp_serializer.data
        return resp

    def pre_save(self, obj):
        obj.library = self.request.user.medialibrary
        super(MediaLibraryAPIView, self).pre_save(obj)

