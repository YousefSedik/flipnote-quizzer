from core.factories import QuizFactory, QuizViewFactory, MCQFactory, WrittenFactory
from rest_framework.test import APITestCase
from accounts.factories import UserFactory
from django.urls import reverse
from .models import Quiz, QuizView, MultipleChoiceQuestion, WrittenQuestion


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


class CreateQuizTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_unauthenticated_creating_quiz(self):
        self.client.force_authenticate(user=None)
        url = reverse("quiz-list-create")
        data = {
            "title": "Test Quiz",
            "description": "This is a test quiz",
            "is_public": True,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_creating_quiz(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("quiz-list-create")
        data = {
            "title": "Test Quiz",
            "description": "This is a test quiz",
            "is_public": True,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(response.data["is_public"], data["is_public"])
        self.assertEqual(response.data["owner_username"], self.user.username)


class DeleteQuizTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.quiz = QuizFactory(owner=self.user)

    def test_deleting_unowned_quiz(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("quiz-retrieve-update-destroy", args=[self.quiz.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Quiz.objects.filter(id=self.quiz.id).exists())

    def test_deleting_owned_quiz(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("quiz-retrieve-update-destroy", args=[self.quiz.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Quiz.objects.filter(id=self.quiz.id).exists())

    def test_deleting_quiz_without_authentication(self):
        self.client.force_authenticate(user=None)
        url = reverse("quiz-retrieve-update-destroy", args=[self.quiz.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)
        self.assertTrue(Quiz.objects.filter(id=self.quiz.id).exists())


class UpdateQuizTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.quiz = QuizFactory(owner=self.user, is_public=True)

    def test_updating_unowned_quiz(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("quiz-retrieve-update-destroy", args=[self.quiz.id])
        data = {
            "title": "Updated Quiz",
            "description": "This is an updated test quiz",
            "is_public": False,
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 403)
        self.quiz.refresh_from_db()
        self.assertNotEqual(self.quiz.title, data["title"])

    def test_updating_owned_quiz(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("quiz-retrieve-update-destroy", args=[self.quiz.id])
        data = {
            "title": "Updated Quiz",
            "description": "This is an updated test quiz",
            "is_public": False,
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.title, data["title"])
        self.assertEqual(self.quiz.description, data["description"])
        self.assertEqual(self.quiz.is_public, data["is_public"])


class CreateQuestionTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.quiz = QuizFactory(owner=self.user)

    def test_unauthenticated_creating_mcq_question(self):
        combinations = [
            {
                "auth": True,
                "is_owner": True,
                "question_type": "mcq",
                "expected_status": 201,
            },
            {
                "auth": True,
                "is_owner": True,
                "question_type": "written",
                "expected_status": 201,
            },
            {
                "auth": True,
                "is_owner": False,
                "question_type": "mcq",
                "expected_status": 403,
            },
            {
                "auth": True,
                "is_owner": False,
                "question_type": "written",
                "expected_status": 403,
            },
            {
                "auth": False,
                "is_owner": False,
                "question_type": "mcq",
                "expected_status": 401,
            },
            {
                "auth": False,
                "is_owner": False,
                "question_type": "written",
                "expected_status": 401,
            },
        ]
        for combo in combinations:
            with self.subTest(combo=combo):
                if combo["auth"]:
                    user = self.user if combo["is_owner"] else self.other_user
                    self.client.force_authenticate(user=user)
                else:
                    self.client.force_authenticate(user=None)

                url = reverse("question-quizzes-create", args=[self.quiz.id])
                if combo["question_type"] == "mcq":
                    data = {
                        "type": "mcq",
                        "text": "What is the capital of France?",
                        "options": ["Paris", "London", "Berlin"],
                        "correct_answer": "Paris",
                    }
                else:
                    data = {
                        "type": "written",
                        "text": "Explain the theory of relativity.",
                        "answer": "The theory of relativity is a scientific theory...",
                    }

                response = self.client.post(url, data=data)

                self.assertEqual(response.status_code, combo["expected_status"])


# class QuizzesHistoryTests(APITestCase):
#     pass
#     def setUp(self):
#         self.user = UserFactory()
#         self.other_user = UserFactory()
#         self.quiz1 = QuizFactory()
#         self.quiz2 = QuizFactory()
#         self.quiz3 = QuizFactory()

#     def test_quiz_history(self):
#         combinations = [
#             {"auth": True, "is_owner": True, "expected_status": 200},
#             {"auth": True, "is_owner": False, "expected_status": 403},
#             {"auth": False, "is_owner": False, "expected_status": 401},
#         ]
