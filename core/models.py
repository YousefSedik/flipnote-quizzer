from django.contrib.auth import get_user_model
from django.db import models
import uuid
from django.utils import timezone

User = get_user_model()


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    views_count = models.SmallIntegerField(default=0, db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")

    def view(self):
        self.views_count += 1
        self.save()

    def __str__(self):
        return self.title


class BaseQuestion(models.Model):
    text = models.TextField(help_text="Enter the question text")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MultipleChoiceQuestion(BaseQuestion):
    quiz = models.ForeignKey(
        "Quiz", on_delete=models.CASCADE, related_name="mcq_questions"
    )
    choices = models.JSONField(default=list, help_text="List of answer choices")
    correct_answer = models.CharField(
        max_length=200, help_text="Enter the correct answer from choices"
    )

    def clean(self):
        if self.correct_answer not in self.choices:
            raise ValueError("Correct answer must be one of the choices")

    def __str__(self):
        return f"{self.text} - {self.correct_answer}"


class WrittenQuestion(BaseQuestion):
    quiz = models.ForeignKey(
        "Quiz", on_delete=models.CASCADE, related_name="written_questions"
    )
    answer = models.TextField(help_text="Enter the correct answer")

    def __str__(self):
        return f"{self.text} - {self.answer}"


class QuizView(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_views")
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("quiz", "user")

    def update_viewed_at(self):
        self.viewed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user} viewed {self.quiz} on {self.viewed_at}"
