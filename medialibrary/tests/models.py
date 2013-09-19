from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from . import TearDownMixin
from ..models import MediaLibrary, AudioShelf, Shelf, Audio, \
    VideoShelf, VideoThumbnail, ImageShelf, Video

class LibraryTest(TestCase):

    def test_library_access(self):
        """Test that library types can be properly accessed"""
        user = User.objects.create(username='testuser')
        self.assertIsInstance(user.medialibrary, MediaLibrary)
        

class ShelfTest(TearDownMixin, TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_shelf_type(self):
        """The proper shelf is always returned"""
        audio = AudioShelf.objects.create(name='testaudio', library=self.user.medialibrary)
        shelves = Shelf.objects.all()
        self.assertIsInstance(shelves[0], AudioShelf)

    def test_file_format_check_on_save(self):
        """The uploaded file should have the proper format, save should be denied otherwise"""
        shelf = AudioShelf.objects.create(name='testaudio', library=self.user.medialibrary)

        media = Audio(file=File(open(__file__, 'rb'), 'testaudio.mp3'))
        shelf.audio_set.add(media)
        self.assertTrue(media.has_valid_format())
        
        media = Audio(file=File(open(__file__, 'rb'), 'testaudio.xxx'))
        self.assertRaises(ValueError, shelf.audio_set.add, media)

    def test_fetching_files_works(self):
        shelf = AudioShelf.objects.create(name='testaudio', library=self.user.medialibrary)
        media = Audio(file=File(open(__file__, 'rb'), 'testaudio.mp3'))
        shelf.audio_set.add(media)

        shelf = AudioShelf.objects.get(pk=shelf.pk)
        self.assertEqual(shelf.audio_set.all()[0], media)

    def test_original_file(self):
        shelf1 = AudioShelf.objects.create(name='testaudio', library=self.user.medialibrary)
        media1 = Audio(file=File(open(__file__, 'rb'), 'testaudio.mp3'), descriptor='original')
        shelf1.audio_set.add(media1)

        shelf2 = VideoShelf.objects.create(name='testVideo', library=self.user.medialibrary)
        media2 = Video(file=File(open(__file__, 'rb'), 'testVideo.mp4'), descriptor='original')
        shelf2.video_set.add(media2)

        self.assertEqual(shelf1.original, media1)
        self.assertEqual(shelf2.original, media2)


class ShelfWithRelationshipTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_relationship_works(self):
        shelf = AudioShelf.objects.create(name='testaudio', library=self.user.medialibrary)
        shelf.relationships.create(relates_to=self.user)
        ct_user = ContentType.objects.get_for_model(self.user)
        shelfrelations = AudioShelf.objects.get(relationships__content_type__pk=ct_user.pk, relationships__object_id=self.user.pk)
        self.assertEqual(shelfrelations, shelf)

    def test_relationshipmanager(self):
        shelf = AudioShelf.objects.create(name='testaudio', library=self.user.medialibrary)
        with self.settings(DEBUG=True):
            shelf.relationships.create(relates_to=self.user)
            from django.db import connection
            q1 = len(connection.queries)
            AudioShelf.with_relations.filter(pk=shelf.pk)
            q2 = len(connection.queries)
            self.assertEqual(q2-q1, 0)
        

class BaseFileTest(TearDownMixin, TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_save_alternative(self):
        shelf = AudioShelf.objects.create(name='testaudio', library=self.user.medialibrary)
        media = Audio(file=File(open(__file__, 'rb'), 'testaudio.mp3'))
        shelf.audio_set.add(media)

        newmedia = media.save_alternative('me/testaudio2.mp3', 'mp3')
        self.assertEqual(shelf.audio_set.count(), 2)
        

class VideoShelfTest(TearDownMixin, TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_thumbnail_set(self):
        shelf = VideoShelf.objects.create(name='testvideo', library=self.user.medialibrary)
        image = ImageShelf.objects.create(name='testimage', library=self.user.medialibrary)
        shelf.thumbnail = image
        self.assertEqual(shelf.thumbnail, image)

    def test_change_thumbnail(self):
        self.test_only_one_thumbnail()
        shelf.thumbnail = image1
        self.assertEqual(shelf.thumbnail, image1)

    def test_thumbnail_get(self):
        shelf = VideoShelf.objects.create(name='testvideo', library=self.user.medialibrary)
        image = ImageShelf.objects.create(name='testimage', library=self.user.medialibrary)
        VideoThumbnail.objects.create(video=shelf, image=image, selected=True)
        self.assertEqual(shelf.thumbnail, image)

    def test_only_one_thumbnail(self):
        shelf = VideoShelf.objects.create(name='testvideo', library=self.user.medialibrary)
        image1 = ImageShelf.objects.create(name='testimage1', library=self.user.medialibrary)
        image2 = ImageShelf.objects.create(name='testimage2', library=self.user.medialibrary)
        VideoThumbnail.objects.create(video=shelf, image=image1, selected=True)
        VideoThumbnail.objects.create(video=shelf, image=image2, selected=True)
        self.assertEqual(shelf.thumbnail, image2)
        return shelf, image1

    def test_change_thumbnail(self):
        shelf, image1 = self.test_only_one_thumbnail()
        shelf.thumbnail = image1
        self.assertEqual(VideoShelf.objects.get(pk=shelf.pk).thumbnail, image1)
