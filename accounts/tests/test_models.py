
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile


class ProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='Mohammed',
            email='test@gmail.com',
            password='123456'
        )

        # الـ Signal أنشأ الـ Profile تلقائياً
        self.profile = Profile.objects.get(user=self.user)

    def test_create_profile(self):
        self.assertIsNotNone(self.profile)
        self.assertEqual(self.profile.user, self.user)

    def test_profile_bio(self):
        self.profile.bio = 'Backend Developer'
        self.profile.save()

        self.assertEqual(self.profile.bio, 'Backend Developer')

    def test_profile_phone(self):
        self.profile.phone = '01012345678'
        self.profile.save()

        self.assertEqual(self.profile.phone, '01012345678')

    def test_profile_str(self):
        self.assertEqual(str(self.profile), 'Mohammed')

    def test_delete_user_cascade(self):
        profile_id = self.profile.id

        self.user.delete()

        self.assertFalse(
            Profile.objects.filter(id=profile_id).exists()
        )
