from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from accounts.factories import UserFactory
from core.models import Quiz
import factory
import uuid

User = get_user_model()


class QuizFactory(DjangoModelFactory):
    class Meta:
        model = Quiz

    id = factory.LazyFunction(uuid.uuid4)
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
    is_public = factory.Faker("boolean")
    owner = factory.SubFactory(UserFactory)
