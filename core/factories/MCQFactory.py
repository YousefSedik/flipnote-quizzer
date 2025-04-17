from core.models import MultipleChoiceQuestion
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from core.factories import QuizFactory
from faker import Faker
import factory

faker = Faker("en_US")
User = get_user_model()
faker.random_choices()
faker.sentences()


class MCQFactory(DjangoModelFactory):
    class Meta:
        model = MultipleChoiceQuestion

    text = factory.Faker("sentence", nb_words=6, variable_nb_words=True)
    options = factory.Faker("words", nb=4, ext_word_list=None)
    answer = factory.Faker("random_element", elements=factory.SelfAttribute("options"))
    quiz = factory.SubFactory(QuizFactory)
