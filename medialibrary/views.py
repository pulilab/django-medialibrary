from django.contrib.contenttypes.models import ContentType

from rest_framework import generics, permissions
from .models import Shelf, ShelfRelation
from .serializers import ShelfSerializer


class AddShelfRelationAPIView(generics.CreateAPIView):
    model = ShelfRelation
    # TODO: should be allowed only for the owner
    permission_classes = (permissions.IsAuthenticated,) 
    
    def post(self, request, *args, **kwargs):
        request.DATA['shelf'] = kwargs['pk']
        request.DATA['content_type'] = ContentType.objects.get_by_natural_key(request.DATA['model'].split('.')[0], request.DATA['model'].split('.')[1]).pk
        resp = super(AddShelfRelationAPIView, self).post(request, *args, **kwargs)
        if resp.status_code == 400 and resp.data.has_key('content_type'):
            resp.data = {'model': "Invalid model given"}
        return resp
        

class MediaLibraryItemView(generics.RetrieveUpdateAPIView):
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

    def get_queryset(self):
        qs = self.model.objects.by_user(self.request.user)
        return qs.exclude(**{'%sshelf__isnull' % self.shelf_type:True})

    def get_serializer_context(self):
        ctx = super(MediaLibraryAPIView, self).get_serializer_context()
        ctx['shelf_type'] = self.shelf_type
        ctx['method'] = self.request.method
        return ctx

    def post(self, request, *args, **kwargs):
        self.shelf_type = kwargs.get('type')
        request.DATA['library'] = self.request.user.medialibrary.pk
        request.DATA['name'] = request.FILES.values()[0].name

        resp = super(MediaLibraryAPIView, self).post(request, *args, **kwargs)
        if not resp.data.has_key('url'):
            return resp
            
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

