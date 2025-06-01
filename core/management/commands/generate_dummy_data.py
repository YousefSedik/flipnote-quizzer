from core.models import Quiz, MultipleChoiceQuestion, WrittenQuestion, QuizView
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        fake = Faker()
        # Create 10 users
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(), email=fake.email(), password="password123"
            )

        # Create 5 quizzes for each user
        for user in User.objects.all():
            for _ in range(5):
                quiz = Quiz.objects.create(
                    title=fake.sentence(),
                    description=fake.text(),
                    owner=user,
                )

                # Create 3 multiple choice questions for each quiz
                for _ in range(3):
                    choices = [fake.word() for _ in range(4)]  # 4 choices
                    MultipleChoiceQuestion.objects.create(
                        quiz=quiz,
                        text=fake.sentence(),
                        choices=choices,
                        correct_answer=fake.random_element(elements=choices),
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                    )

                # Create 2 written questions for each quiz
                for _ in range(2):
                    WrittenQuestion.objects.create(
                        quiz=quiz,
                        text=fake.sentence(),
                        answer=fake.sentence(),
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                    )

        self.stdout.write(self.style.SUCCESS("Successfully generated dummy data."))
        # Create 5 quiz views for each quiz
        for quiz in Quiz.objects.all():
            for _ in range(5):
                try:
                    QuizView.objects.create(
                        quiz=quiz,
                        user=fake.random_element(elements=User.objects.all()),
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error creating quiz view: {e}")
                    )
                    continue
        self.stdout.write(
            self.style.SUCCESS("Successfully generated dummy quiz views.")
        )
