from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Shelf
from .serializers import ShelfSerializer
#from vidzor.videoupload.serializers import VideoSerializer


class MediaLibraryAPIView(generics.ListCreateAPIView):
    """Retrieves and creates shelves of a given type from the MediaLibrary"""
    model = Shelf
    serializer_class = ShelfSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        self.shelf_type = kwargs.get('type')
        self.user = request.user
        return super(MediaLibraryAPIView, self).get(request, *args, **kwargs)

    def get_serializer_context(self):
        ctx = super(MediaLibraryAPIView, self).get_serializer_context()
        ctx['shelf_type'] = self.shelf_type
        return ctx


# class GenericLibraryAPI(generics.ListCreateAPIView):
#     model = MediaLibrary
#     model_type = None
#     user = None
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request, *args, **kwargs):
#         self.model_type = kwargs.get('type')
#         self.user = request.user
#         return super(GenericLibraryAPI, self).get(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         self.model_type = kwargs.get('type')
#         self.user = request.user

#         # Forbid using this method to upload videofiles, use old /v2/api/upload
#         # till it's not refactored.
#         # TODO: refactor and remove /v2/api/upload
#         if self.model_type == 'video':
#             return Response({'error': 'not implemented yet, use old videouploader'},
#                             status=status.HTTP_403_FORBIDDEN)
#         return super(GenericLibraryAPI, self).post(request, *args, **kwargs)

#     def pre_save(self, obj):
#         obj.user = self.user
#         super(GenericLibraryAPI, self).pre_save(obj)

#     def post_save(self, obj, created=False):
#         if created:
#             # Add uploaded object to user's library
#             self.get_library().add(obj)
#         super(GenericLibraryAPI, self).post_save(obj, created)

#     def get_serializer_class(self):
#         if self.model_type == 'video':
#             return VideoSerializer
#         elif self.model_type == 'audio':
#             return AudioSerializer
#         elif self.model_type == 'image':
#             return ImageSerializer

#     def get_library(self):
#         """
#         Return the proper type of library of the user
#         """
#         library = self.model.objects.get(user=self.user)

#         libraries = {
#             'video': library.video.files,
#             'audio': library.audio.files,
#             'image': library.image.files
#         }
#         return libraries[self.model_type]

#     def get_queryset(self):
#         return self.get_library().all()

