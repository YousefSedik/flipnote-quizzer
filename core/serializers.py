from rest_framework import serializers
from .models import (
    Quiz,
    MultipleChoiceQuestion,
    WrittenQuestion,
)


class QuizSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Quiz
        exclude = ("owner",)


class MCQSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(
        queryset=Quiz.objects.all(), write_only=True
    )

    class Meta:
        model = MultipleChoiceQuestion
        exclude = ("created_at", "updated_at")


class WrittenQuestionSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(
        queryset=Quiz.objects.all(), write_only=True
    )

    class Meta:
        model = WrittenQuestion
        exclude = ("created_at", "updated_at")


class QuestionsSerializer(serializers.Serializer):
    mcq_questions = MCQSerializer(many=True)
    written_questions = WrittenQuestionSerializer(many=True)
    quiz = QuizSerializer()

    class Meta:
        fields = ("mcq_questions", "written_questions", "quiz")

class GeneralQuestionSerializer(serializers.Serializer):
    text = serializers.CharField()
    answer = serializers.CharField()
    correct_answer = serializers.CharField()
    options = serializers.ListField(child=serializers.CharField(), allow_empty=True)

    class Meta:
        fields = ("text", "answer", "correct_answer", "options")