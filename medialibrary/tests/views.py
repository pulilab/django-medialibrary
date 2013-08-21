import json
from django.test import TestCase
from django.core.files import File
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ..models import AudioShelf, Audio
from ..serializers import ShelfSerializer

class LibraryViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('alma', 'alma@example.com', 'alma')

    def _login(self):
        login = self.client.login(username='alma', password='alma')
        self.assertTrue(login)

    def test_upload_image(self):
        self._login()
        with open('resources/test.png') as fp:
            resp = self.client.post(reverse('medialibrary',
                                            kwargs={'type':'image'}),
                                    {'file': fp})
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        self.assertEqual(data['name'], 'test.png')
        self.assertEqual(len(data['files']), 1)


class LibraryLoadedViewTest(TestCase):

    # fixtures = ['test_library.json']

    def setUp(self):
        self.user = User.objects.create_user('alma', 'alma@example.com', 'alma')
        self.shelf = AudioShelf.objects.create(name='testaudio', library=self.user.medialibrary)
        media1 = Audio(file=File(open(__file__, 'rb'), 'testaudio.mp3'))
        media2 = Audio(file=File(open(__file__, 'rb'), 'testaudio.mp3'))
        self.shelf.audio_set.add(media1)
        self.shelf.audio_set.add(media2)

    def _login(self):
        login = self.client.login(username='alma', password='alma')
        self.assertTrue(login)

    def test_get_images(self):
        self._login()
        resp = self.client.get(reverse('medialibrary', kwargs={'type':'audio'}))
        self.assertEqual(resp.status_code, 200)
        keys_to_match = json.loads(resp.content)[0].keys()
        keys_to_match.sort()
        serializer_keys = ShelfSerializer(self.shelf, context={'shelf_type': 'audio'}).data.keys()
        serializer_keys.sort()
        self.assertEqual(
            keys_to_match, 
            serializer_keys
        )