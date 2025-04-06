from rest_framework import serializers
from .models import Quiz, MultipleChoiceQuestion, WrittenQuestion, QuizView


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"
