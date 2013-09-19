import json
from django.test import TestCase
from django.core.files import File
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from . import TearDownMixin
from ..models import AudioShelf, Audio
from ..serializers import ShelfSerializer

class MyViewTestMixin(object):

    def _create_user(self, username='alma'):
        self.user = User.objects.create_user(username, '%s@example.com' % username, username)

    def _login(self):
        login = self.client.login(username='alma', password='alma')
        self.assertTrue(login)


class AddShelfRelationAPIView(MyViewTestMixin, TestCase):

    def setUp(self):
        self._create_user()
        self.shelf = AudioShelf.objects.create(name='testaudio', library=self.user.medialibrary)

    def test_requires_login(self):
        resp = self.client.post(reverse('medialibrary-shelf-add-relation', kwargs={'pk':self.shelf.pk}), 
            data={})
        self.assertEqual(resp.status_code, 403)

    def test_add_relationship(self):
        self._login()
        resp = self.client.post(reverse('medialibrary-shelf-add-relation', kwargs={'pk':self.shelf.pk}), 
            data={'model':'auth.user', 'object_id':self.user.pk})
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertEqual(self.shelf.relationships.count(), 1)

    def test_relationships_are_restricted(self):
        self._login()
        resp = self.client.post(reverse('medialibrary-shelf-add-relation', kwargs={'pk':self.shelf.pk}), 
            data={'model':'medialibrary.medialibrary', 'object_id':self.user.medialibrary.pk})
        self.assertEqual(resp.status_code, 400, resp.content)
        data = json.loads(resp.content)
        self.assertTrue(data.has_key('model'))


class LibraryViewTest(TearDownMixin, MyViewTestMixin, TestCase):

    def setUp(self):
        self._create_user()

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


class LibraryLoadedViewTest(TearDownMixin, MyViewTestMixin, TestCase):

    # fixtures = ['test_library.json']

    def setUp(self):
        self._create_user()
        self.shelf = AudioShelf.objects.create(name='testaudio', library=self.user.medialibrary)
        media1 = Audio(file=File(open(__file__, 'rb'), 'testaudio.mp3'))
        media2 = Audio(file=File(open(__file__, 'rb'), 'testaudio.mp3'))
        self.shelf.audio_set.add(media1)
        self.shelf.audio_set.add(media2)

    def test_get_audio(self):
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

    def test_returned_items(self):
        """VIDZOR-311"""
        self._login()
        resp = self.client.get(reverse('medialibrary', kwargs={'type':'video'}))
        data = json.loads(resp.content)
        self.assertEqual(data, [])


class LibraryPermissionTest(TearDownMixin, MyViewTestMixin, TestCase):

    def setUp(self):
        self._create_user()
        self.username2 = 'alma2'
        self.user2 = User.objects.create_user(self.username2, '%s@example.com' % self.username2, self.username2)

        # upload a testaudio file for user2
        self.shelf = AudioShelf.objects.create(name='testaudio', library=self.user2.medialibrary)
        media = Audio(file=File(open(__file__, 'rb'), 'testaudio.mp3'))
        self.shelf.audio_set.add(media)

    def test_audioshelf_permission(self):
        # login with alma2
        login = self.client.login(username=self.username2, password=self.username2)
        self.assertTrue(login)

        # get audio with alma2
        resp = self.client.get(reverse('medialibrary', kwargs={'type':'audio'}))
        self.assertContains(resp, 'testaudio')

        # logout and login with other user
        self.client.logout()
        self._login()

        # other user should not see the testaudio file
        resp = self.client.get(reverse('medialibrary', kwargs={'type':'audio'}))
        self.assertNotContains(resp, 'testaudio')