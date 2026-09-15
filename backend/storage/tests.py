import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase
from users.models import User
from storage.models import File


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class StorageApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='User1234', full_name='User', email='u@example.com', password='Strong1!')
        self.other = User.objects.create_user(username='Other123', full_name='Other', email='o@example.com', password='Strong1!')
        self.admin = User.objects.create_user(username='Admin123', full_name='Admin', email='a@example.com', password='Strong1!', is_admin=True)
        self.file = File.objects.create(user=self.user, original_name='test.txt', file=SimpleUploadedFile('test.txt', b'hello'), size=5, comment='c')

    def test_owner_can_list_own_files(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/api/files/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_other_user_cannot_download_file(self):
        self.client.force_authenticate(self.other)
        response = self.client.get(f'/api/files/{self.file.id}/download/')
        self.assertEqual(response.status_code, 404)

    def test_admin_can_select_user_storage(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(f'/api/files/?user_id={self.user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['original_name'], 'test.txt')

    def test_public_info_does_not_expose_owner_or_token(self):
        response = self.client.get(f'/api/public/files/{self.file.share_token}/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('owner_username', response.data)
        self.assertNotIn('share_token', response.data)
