from django.urls import path

from . import views
from .views import Question, Answers, AnswerMVP

urlpatterns = [
#    path('list_category', views.get_list_category, name='list_category'),
    path('api/question', Question.as_view()),
    path('api/answer', Answers.as_view()),
    path('', AnswerMVP.as_view()),


    #path('list_question', views.post_for_question, name='question'),

]
