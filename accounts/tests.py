from accounts.factories import UserFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse


User = get_user_model()


class UsersManagersTests(APITestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com",
            password="foo",
            username="normal_user",
            first_name="Normal",
            last_name="User",
        )
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com",
            password="foo",
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )


class UsersTestCases(APITestCase):
    def test_registering_users(self):
        # create user1, user2
        self.user1 = {
            "first_name": "yousef",
            "last_name": "sedik",
            "username": "yousef",
            "email": "random_email@gmail.com",
            "password": "strong_password1@",
            "password2": "strong_password1@",
        }
        response = self.client.post(reverse("accounts:create_user"), data=self.user1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], self.user1["email"])
        self.assertEqual(response.data["first_name"], self.user1["first_name"])
        self.assertEqual(User.objects.all().count(), 1)
