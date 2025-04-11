from .serializers import QuizSerializer, QuestionSerializer
from .pagination import CustomPageNumberPagination
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly, IsOwnerOrPublic
from .models import Quiz


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
        return super().get_queryset().filter(owner=self.request.user)


quiz_list_create = MyQuizListCreate.as_view()


class QuizRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [
        IsOwnerOrPublic,
    ]


quiz_retrieve_update_destroy = QuizRetrieveUpdateDestroyAPIView.as_view()


class QuestionRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = QuestionSerializer
    lookup_field = "pk"
    permission_classes = [IsOwnerOrPublic]

    def get_object(self):
        quiz_id = self.kwargs.get(self.lookup_field)

        quiz = (
            Quiz.objects.filter(id=quiz_id)
            .prefetch_related("mcq_questions", "written_questions")
            .first()
        )
        if not quiz:
            raise NotFound("Quiz not found")

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


# class CreateQuestion(generics.CreateAPIView):
#     serializer_class = QuestionSerializer
