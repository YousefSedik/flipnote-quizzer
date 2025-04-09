from django.urls import path
from .api import quiz_list_create, quiz_retrieve_update_destroy, question_list_create

urlpatterns = [
    path("quizzes", quiz_list_create, name="quiz-list-create"),
    path(
        "quizzes/<uuid:pk>", quiz_retrieve_update_destroy, name="quiz-retrieve-update-destroy"
    ),
    path("questions/<uuid:pk>", question_list_create, name="question-list-create"),
]
