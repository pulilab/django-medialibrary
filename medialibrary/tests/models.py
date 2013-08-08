from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase

from ..models import MediaLibrary, AudioShelf, Shelf, Audio

class LibraryTest(TestCase):

    def test_library_access(self):
        """Test that library types can be properly accessed"""
        user = User.objects.create(username='testuser')
        self.assertIsInstance(user.medialibrary, MediaLibrary)
        

class ShelfTest(TestCase):

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
        