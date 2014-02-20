from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from jsonfield import JSONField

from model_utils import Choices
from model_utils.models import TimeStampedModel
from model_utils.managers import InheritanceManager
#from thumbnail_works.fields import EnhancedImageField

from .utils import setup_upload_route, content_type_restriction

class ShelfManager(InheritanceManager):

    def get_query_set(self):
        return super(ShelfManager, self).get_query_set().select_subclasses().prefetch_related('audio_set', 'video_set', 'image_set')

    def by_user(self, user):
        return self.get_query_set().filter(library__user=user)


class ShelfManagerWithRelations(ShelfManager):

    def get_query_set(self):
        return super(ShelfManagerWithRelations, self).get_query_set().prefetch_related('shelfrelation_set')


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
    with_relations = ShelfManagerWithRelations()

    def file_set():
        doc = "The file_set property."
        def fget(self):
            raise NotImplementedError
        return locals()
    file_set = property(**file_set())

    class Meta:
        verbose_name_plural = 'Shelves'

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.__class__)

    @models.permalink
    def get_absolute_url(self):
        return ('medialibrary-shelf', (), {'pk': self.pk})

    def original():
        doc = "The original file"
        def fget(self):
            return self.file_set.filter(descriptor='original')[0]
        return locals()
    original = property(**original())

    def size():
        doc = "The size of the original file"
        def fget(self):
            return self.original.file.size
        return locals()
    size = property(**size())

    def url():
        doc = "The url of the original file"
        def fget(self):
            return self.original.file.url
        return locals()
    url = property(**url())


class ShelfRelation(TimeStampedModel):
    shelf = models.ForeignKey(Shelf, related_name='relationships')
    content_type = models.ForeignKey(ContentType, limit_choices_to=content_type_restriction)
    object_id = models.PositiveIntegerField()
    relates_to = generic.GenericForeignKey('content_type', 'object_id')


class AudioShelf(Shelf):

    # AVAILABLE_FORMATS = ('aac', 'ogg', 'webm')
    ALLOWED_FORMATS = ('mp3', 'aac', 'ogg', 'webm')

    def file_set():
        doc = "The file_set property."
        def fget(self):
            return self.audio_set
        return locals()
    file_set = property(**file_set())


class VideoShelf(Shelf):
    
    # AVAILABLE_FORMATS = ('mp4', 'webm')
    ALLOWED_FORMATS = (
    '3gp', 'asf', 'avi', 'divx', 'flv', 'mkv', 'mov', 'mpg', 'mp4', 'mpeg',
    'm4v', 'mxf', 'ogg', 'vob', 'webm')
    thumbnails = models.ManyToManyField('ImageShelf', through='VideoThumbnail', null=True, blank=True)

    def file_set():
        doc = "The file_set property."
        def fget(self):
            return self.video_set
        return locals()
    file_set = property(**file_set())

    def thumbnail():
        doc = "The video's thumbnail"
        def fget(self):
            try:
                return VideoThumbnail.objects.get_selected(video=self).image
            except VideoThumbnail.DoesNotExist:
                return None
        def fset(self, imageShelf):
            try:
                thumbnail = VideoThumbnail.objects.get(video=self, image=imageShelf)
            except VideoThumbnail.DoesNotExist:
                VideoThumbnail.objects.create(video=self, image=imageShelf, selected=True)
            else:
                thumbnail.selected = True
                thumbnail.save()
        return locals()
    thumbnail = property(**thumbnail())

    def duration():
        doc = "The length property."
        def fget(self):
            return self.original.duration
        return locals()
    duration = property(**duration())


class ImageShelf(Shelf):

    ALLOWED_FORMATS = ('jpg', 'jpeg', 'gif', 'png', 'pdf')

    def file_set():
        doc = "The file_set property."
        def fget(self):
            return self.image_set
        return locals()
    file_set = property(**file_set())


class ThumbnailManager(models.Manager):
    use_for_related_fields = True

    def get_selected(self, **kwargs):
        kwargs.update({'selected': True})
        return self.get_query_set().get(**kwargs)


class VideoThumbnail(models.Model):

    video = models.ForeignKey(VideoShelf)
    image = models.ForeignKey(ImageShelf)
    selected = models.BooleanField(default=False)

    objects = ThumbnailManager()

    def save(self, **kwargs):
        if self.selected == True:
            VideoThumbnail.objects.filter(video=self.video).update(selected=False)
        return super(VideoThumbnail, self).save(**kwargs)

class BaseFile(TimeStampedModel):
    """
        BaseFile abstract class that defines all the common characters.
    """
    shelf = models.ForeignKey(Shelf)
    descriptor = models.CharField(max_length=255, blank=True, default='original')
    content_type = models.CharField(max_length=50, blank=True, default='application/octet-stream')
    file = models.FileField(max_length=255, upload_to=setup_upload_route)
    meta = JSONField(blank=True, help_text="An arbitrary JSON")

    class Meta:
        abstract = True

    def has_valid_format(self):
        return self.file.url.split('.')[-1].lower() in self.shelf.ALLOWED_FORMATS

    def save(self, force_insert=False, force_update=False, update_fields=None):
        if not self.has_valid_format():
            raise ValueError
        return super(BaseFile, self).save(force_insert, force_update, update_fields)

    def save_alternative(self, url, descriptor, meta={}, **kwargs):
        """Creates a new media record in the DB from the current one without saving any new files in the storage"""
        self.pk = None
        self.file.name = url
        self.descriptor = descriptor
        self.meta = meta if meta else self.meta
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
        return self


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

    duration = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    width = models.IntegerField(null=True)


class Image(BaseFile):
    TYPES = Choices('original', 'thumbnail')


class MediaLibrary(TimeStampedModel):
    """
        Media Library for a user, it aggregates the three other sublibraries,
        so the user can easily reach them.
    """

    user = models.OneToOneField(User)

    def __unicode__(self):
        return 'Library for user %s' % self.user.username

@receiver(post_save, sender=User, dispatch_uid="create_media_library")
def create_media_library(sender, created, instance, **kwargs):
    if created:
        instance.medialibrary, created = MediaLibrary.objects.get_or_create(user=instance)
        instance.save()
