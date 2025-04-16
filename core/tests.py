from core.factories import QuizFactory, QuizViewFactory, MCQFactory, WrittenFactory
from rest_framework.test import APITestCase
from accounts.factories import UserFactory
from django.urls import reverse


class QuizAccessTests(APITestCase):
    def setUp(self):
        self.owner = UserFactory()
        self.other_user = UserFactory()

    def test_quiz_access_combinations(self):
        combinations = [
            {"auth": True, "public": False, "is_owner": True, "expected_status": 200},
            {"auth": True, "public": True, "is_owner": True, "expected_status": 200},
            {"auth": True, "public": True, "is_owner": False, "expected_status": 200},
            {"auth": True, "public": False, "is_owner": False, "expected_status": 403},
            {"auth": False, "public": False, "is_owner": False, "expected_status": 401},
            {"auth": False, "public": True, "is_owner": False, "expected_status": 200},
        ]

        for combo in combinations:
            with self.subTest(combo=combo):
                quiz_owner = self.owner
                quiz = QuizFactory(is_public=combo["public"], owner=quiz_owner)

                if combo["auth"]:
                    user = self.owner if combo["is_owner"] else self.other_user
                    self.client.force_authenticate(user=user)
                else:
                    self.client.force_authenticate(user=None)

                url = reverse("quiz-retrieve-update-destroy", args=[quiz.id])
                response = self.client.get(url)

                self.assertEqual(response.status_code, combo["expected_status"])
