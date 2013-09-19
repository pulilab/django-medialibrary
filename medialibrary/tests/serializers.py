from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files import File
from . import TearDownMixin
from ..serializers import ShelfSerializer, AudioSerializer
from ..models import ImageShelf, Image, AudioShelf, Audio


class BaseFileSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('alma', 'alma@example.com', 'alma')
    
    def test_audio_serializer_return_values(self):
        shelf = AudioShelf.objects.create(name='testaudio', library=self.user.medialibrary)
        audio = Audio(file=File(open(__file__, 'rb'), 'testaudio.mp3'))
        # shelf.audio_set.add(media)

        serializer = AudioSerializer(audio)
        self.assertEqual(serializer.data.keys(), ['file', 'descriptor', 'meta', 'url'])
        self.assertEqual(serializer.data['url'], 'testaudio.mp3')


class ShelfSerializerTest(TearDownMixin, TestCase):

    def setUp(self):
        self.user = User.objects.create_user('alma', 'alma@example.com', 'alma')

    def test_create_shelf_with_file(self):
        data = {
            'name': 'Example',
            'library': self.user.medialibrary.pk,
        }
        files = {'file': File(open(__file__, 'rb'), 'testimage.png')}
        context = {
            'shelf_type': 'image',
            'method': 'POST',
        }
        serialized = ShelfSerializer(data=data, files=files, context=context)
        self.assertTrue(serialized.is_valid(), str(serialized.errors))
        shelf = serialized.save()
        
        s1 = ImageShelf.objects.all()[0]
        self.assertEqual(shelf, s1)
        self.assertEqual(shelf.image_set.all()[0], Image.objects.all()[0])

    def test_get_shelf_with_files(self):
        shelf = AudioShelf.objects.create(name='testaudio', library=self.user.medialibrary)
        media = Audio(file=File(open(__file__, 'rb'), 'testaudio.mp3'))
        shelf.audio_set.add(media)

        context = {
            'shelf_type': 'audio',
        }
        serializer = ShelfSerializer(shelf, context=context)
        self.assertEqual(len(serializer.data['audio_set']), 1)
        self.assertEqual(len(serializer.data['files']), 1)

        fileSerializer = AudioSerializer(media)
        self.assertEqual(serializer.data['audio_set'], [fileSerializer.data])
        self.assertEqual(serializer.data['files'], [fileSerializer.data])
