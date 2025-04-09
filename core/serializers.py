from rest_framework import serializers
from .models import (
    Quiz,
    BaseQuestion,
    MultipleChoiceQuestion,
    WrittenQuestion,
    QuizView,
)


class QuizSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Quiz
        exclude = ("owner",)


class MCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceQuestion
        exclude = ("quiz", "created_at", "updated_at")


class WrittenQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenQuestion
        exclude = ("quiz", "created_at", "updated_at")


class QuestionSerializer(serializers.Serializer):
    mcq_questions = MCQSerializer(many=True)
    written_questions = WrittenQuestionSerializer(many=True)
    quiz = QuizSerializer()

    class Meta:
        fields = ("mcq_questions", "written_questions", "quiz")


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseQuestion
