from django.urls import path, re_path

from . import views
from .views import Question, Answers, AnswerMVP, LoginAPIView

urlpatterns = [
    path('api/question', Question.as_view()),
    path('api/answer', Answers.as_view()),
    path('', AnswerMVP.as_view()),
    re_path(r'^login/?$', LoginAPIView.as_view(), name='user_login'),
]
