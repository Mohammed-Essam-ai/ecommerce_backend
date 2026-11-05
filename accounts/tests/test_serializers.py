
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile
from accounts.serializers import ProfileSerializer


class ProfileSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='123456'
        )

        self.profile = self.user.profile

        self.profile.bio = 'Test bio'
        self.profile.phone = '01012345678'
        self.profile.save()

    def test_serialize_profile(self):

        serializer = ProfileSerializer(self.profile)

        self.assertEqual(serializer.data['bio'], 'Test bio')
        self.assertEqual(serializer.data['phone'], '01012345678')