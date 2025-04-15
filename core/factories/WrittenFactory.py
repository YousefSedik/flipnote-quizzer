from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from core.models import WrittenQuestion
from core.factories import QuizFactory
import factory

User = get_user_model()


class WrittenQuestionFactory(DjangoModelFactory):
    class Meta:
        model = WrittenQuestion

    text = factory.Faker("sentence")
    answer = factory.Faker("sentence")
    quiz = factory.SubFactory(QuizFactory)
