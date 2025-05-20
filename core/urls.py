from django.urls import path
from .api import (
    quiz_list_create,
    quiz_retrieve_update_destroy,
    question_list_create,
    public_quiz_api_view,
    create_question_api_view,
    delete_question_api_view,
    quiz_history_list_api_view,
    extract_questions,
    quiz_search,
)

urlpatterns = [
    path("quizzes", quiz_list_create, name="quiz-list-create"),
    path(
        "quizzes/<uuid:pk>",
        quiz_retrieve_update_destroy,
        name="quiz-retrieve-update-destroy",
    ),
    path("questions/<uuid:pk>", question_list_create, name="question-list-create"),
    path("quizzes/public", public_quiz_api_view, name="public-quizzes"),
    path(
        "quizzes/<uuid:pk>/questions",
        create_question_api_view,
        name="question-quizzes-create",
    ),
    path(
        "quizzes/<uuid:pk>/questions/<int:question_id>/<str:qtype>",
        delete_question_api_view,
        name="question-delete",
    ),
    path("quizzes/history", quiz_history_list_api_view, name="view-history-list"),
    path("extract-questions", extract_questions, name="extract-questions"),
    path("quiz/search", quiz_search, name="search-quiz"),
]
