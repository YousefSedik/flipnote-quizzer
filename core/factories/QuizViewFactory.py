from core.models import QuizView, Quiz
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
import factory

User = get_user_model()


class QuizViewFactory(DjangoModelFactory):
    class Meta:
        model = QuizView

    quiz = factory.Iterator(Quiz.objects.all())
    user = factory.Iterator(User.objects.all())
    viewed_at = factory.Faker("date_time_this_year")
