import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from jsonfield import JSONField

from model_utils import Choices
from model_utils.models import TimeStampedModel
from model_utils.managers import InheritanceManager
#from thumbnail_works.fields import EnhancedImageField

from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage()

def setup_upload_route(instance, filename=None):
    today = datetime.datetime.today()
    return '%s/%s-%02d-%02d/%s' % (instance.shelf.__class__.__name__.lower(),
                                       today.year, today.month, today.day,
                                       filename)


class ShelfManager(InheritanceManager):

    def get_query_set(self):
        return super(ShelfManager, self).get_query_set().select_subclasses().prefetch_related('audio_set', 'video_set')


class Shelf(TimeStampedModel):
    STATE_CHOICES = Choices(
            (0, 'unconverted', 'Unconverted'),
            (1, 'converted', 'Converted')
        )
    state = models.CharField(choices=STATE_CHOICES, default=STATE_CHOICES.unconverted,
                                db_index=True, max_length=2)
    name = models.CharField(max_length=255)
    library = models.ForeignKey('MediaLibrary')

    objects = ShelfManager()        


class AudioShelf(Shelf):

    # AVAILABLE_FORMATS = ('aac', 'ogg', 'webm')
    ALLOWED_FORMATS = ('mp3', 'aac', 'ogg', 'webm')


class VideoShelf(Shelf):
    
    # AVAILABLE_FORMATS = ('mp4', 'webm')
    ALLOWED_FORMATS = ('mp4', 'webm', 'avi')


class ImageShelf(Shelf):

    ALLOWED_FORMATS = ('jpg', 'jpeg', 'gif', 'png', 'pdf')


class BaseFile(TimeStampedModel):
    """
        BaseFile abstract class that defines all the common characters.
    """
    shelf = models.ForeignKey(Shelf)
    descriptor = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=setup_upload_route, storage=fs)
    meta = JSONField(blank=True)

    #user = models.ForeignKey(User)
    #project = models.ForeignKey(Project, null=True, blank=True,
    #                            related_name='%(app_label)s_%(class)s_set')

    class Meta:
        abstract = True

    def has_valid_format(self):
        return self.file.url.split('.')[-1] in self.shelf.ALLOWED_FORMATS

    def save(self, force_insert=False, force_update=False, update_fields=None):
        if not self.has_valid_format():
            raise ValueError
        return super(BaseFile, self).save(force_insert, force_update, update_fields)


class Audio(BaseFile):
    """
        Audio model to store audiofiles that can be added to a project.
    """
    TYPES = Choices('original', 'webm', 'mp3')


class Video(BaseFile):
    """
    Audio model to store audiofiles that can be added to a project.
    """
    TYPES = Choices('original', 'webm', 'mp4')


class Image(BaseFile):
    TYPES = Choices('original', 'thumbnail')


# class Image(BaseFile):
#     """
#         Image model to store images with thumbnails.
#     """

#     imagefile = EnhancedImageField(
#         upload_to=setup_upload_route,
#         storage=fs,
#         #process_source = dict(size='512x384', sharpen=True, upscale=True, format='JPEG'),
#         thumbnails={
#             'thumb': dict(size='128x128')
#         }
#     )

# try:
#     from south.modelsinspector import add_introspection_rules
#     add_introspection_rules([], ["^thumbnail_works.fields.EnhancedImageField"])
# except ImportError:
#     pass

# class Library(TimeStampedModel):
#     """
#         BaseLibrary abstract class defines common timestamps and title for
#         user's libraries.
#     """

#     title = models.CharField(blank=True, max_length=200)


# class VideoLibrary(Library):

#     AVAILABLE_FORMATS = ('mp4', 'webm')
#     ALLOWED_FORMATS = ('mp4', 'webm', 'avi')

#     files = models.ManyToManyField('videoupload.Video')


# class AudioLibrary(Library):

#     AVAILABLE_FORMATS = ('aac', 'ogg')
#     ALLOWED_FORMATS = ('mp3', 'aac', 'ogg')

#     files = models.ManyToManyField(Audio)


# class ImageLibrary(Library):

#     AVAILABLE_FORMATS = ('jpg',)
#     ALLOWED_FORMATS = ('jpg', 'png', 'gif')

#     files = models.ManyToManyField(Image)


class MediaLibrary(TimeStampedModel):
    """
        Media Library for a user, it aggregates the three other sublibraries,
        so the user can easily reach them.
    """

    user = models.OneToOneField(User)

    # video = models.OneToOneField(VideoLibrary, null=True, blank=True)
    # audio = models.OneToOneField(AudioLibrary, null=True, blank=True)
    # image = models.OneToOneField(ImageLibrary, null=True, blank=True)

    def __unicode__(self):
        return 'Library for user %s' % self.user.username

@receiver(post_save, sender=User, dispatch_uid="create_media_library")
def create_media_library(sender, created, instance, **kwargs):
    if created:
        instance.medialibrary = MediaLibrary.objects.create(user=instance)
        instance.save()

# @receiver(post_save, sender=MediaLibrary, dispatch_uid="create_all_libraries")
# def create_all_libraries(sender, created, instance, **kwargs):
#     if created:
#         instance.video = VideoLibrary.objects.create()
#         instance.audio = AudioLibrary.objects.create()
#         # instance.image = ImageLibrary.objects.create()
#         instance.save()


# Create your models here.
