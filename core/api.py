from .serializers import (
    QuizSerializer,
    QuestionsSerializer,
    WrittenQuestionSerializer,
    MCQSerializer,
)
from .models import Quiz, QuizView, MultipleChoiceQuestion, WrittenQuestion
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, ValidationError
from .permissions import IsOwnerOrReadOnly, IsQuizOwner
from .pagination import CustomPageNumberPagination
from rest_framework import generics, permissions
from .services import get_content, get_questions
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from urllib.parse import unquote
from django.db.models import Q
import json


class MyQuizListCreate(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Quiz.objects.filter(owner=self.request.user).prefetch_related("owner")


quiz_list_create = MyQuizListCreate.as_view()


class QuizRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        quiz = super().get_object()
        if self.request.user.is_authenticated:
            user = self.request.user
            # print(quiz[0])
            QuizView.objects.update_or_create(
                user=user,
                quiz=quiz,
                defaults={"viewed_at": timezone.now()},
            )
        return quiz


quiz_retrieve_update_destroy = QuizRetrieveUpdateDestroyAPIView.as_view()


class QuestionRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = QuestionsSerializer
    lookup_field = "pk"
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        quiz_id = self.kwargs.get(self.lookup_field)

        quiz = (
            Quiz.objects.filter(id=quiz_id)
            .prefetch_related("mcq_questions", "written_questions")
            .first()
        )
        if not quiz:
            raise NotFound("Quiz not found")

        if self.request.user.is_authenticated:
            quiz_view, created = QuizView.objects.get_or_create(
                user=self.request.user, quiz=quiz
            )
            if not created:
                quiz_view.update_viewed_at()

        quiz.view()
        mcq_questions = quiz.mcq_questions.all()
        written_questions = quiz.written_questions.all()

        return {
            "quiz": quiz,
            "mcq_questions": mcq_questions,
            "written_questions": written_questions,
        }

    def retrieve(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = self.get_serializer(data)
        return Response(serializer.data)


question_list_create = QuestionRetrieveAPIView.as_view()


class PublicQuizAPIView(generics.ListAPIView):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    pagination_class = CustomPageNumberPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return super().get_queryset().filter(is_public=True)


public_quiz_api_view = PublicQuizAPIView.as_view()


class CreateQuestionAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsQuizOwner]

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:

            data = kwargs["data"].copy()
            data["quiz"] = self.request.resolver_match.kwargs["pk"]
            question_type = data.pop("type", "")
            if question_type == "written":
                return WrittenQuestionSerializer(data=data)
            elif question_type == "mcq":
                return MCQSerializer(data=data)
            else:
                raise ValidationError(
                    f"Question type '{question_type}' is not supported"
                )

        return super().get_serializer(*args, **kwargs)


create_question_api_view = CreateQuestionAPIView.as_view()


class DeleteQuestionAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsQuizOwner]

    def get_object(self):
        question_type = self.request.resolver_match.kwargs["qtype"]
        question_id = self.request.resolver_match.kwargs["question_id"]
        if question_type == "mcq":
            return get_object_or_404(MultipleChoiceQuestion, pk=question_id)
        elif question_type == "written":
            return get_object_or_404(WrittenQuestion, pk=question_id)


delete_question_api_view = DeleteQuestionAPIView.as_view()


class QuizHistoryListAPIView(generics.ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        history = (
            QuizView.objects.filter(
                Q(user=self.request.user)
                & (Q(quiz__is_public=True) | Q(quiz__owner=self.request.user))
            )
            .values("quiz")
            .order_by("-viewed_at")
        )[:3]
        print(history)
        if not history:
            raise NotFound("No quiz history found")
        return Quiz.objects.filter(Q(id__in=history) & (Q(is_public=True) | Q(owner=self.request.user)))[:3]


quiz_history_list_api_view = QuizHistoryListAPIView.as_view()


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def extract_questions(request):
    uploaded_file = request.FILES.get("file")
    content, success = "", False
    if uploaded_file is None:
        data = request.body
        data = json.loads(unquote(str(data, encoding="utf-8")))
        content = data.get("text")
        if content is None:
            return Response(
                {"error": "file not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            success = True
    else:
        content, success, err = get_content(uploaded_file)
    if not success:
        return Response({"error": err}, status.HTTP_400_BAD_REQUEST)

    mcqs, written = get_questions(content)
    return Response({"mcqs": mcqs, "written": written})


@api_view(["GET"])
@permission_classes([])
def quiz_search(request):
    query: str = request.GET.get("q", "")

    if query.strip():
        results = Quiz.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )[:5]
        serializer = QuizSerializer(results, many=True)
        return Response(serializer.data)

    return Response([], status=200)
