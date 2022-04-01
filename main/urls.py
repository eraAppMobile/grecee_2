
from django.urls import path, re_path

from . import views
from .views import Question, Answers, AnswerMVP, LoginAPIView, logout_user, login_site

urlpatterns = [

    path('api/question', Question.as_view()),
    path('api/answer', Answers.as_view()),
    path('mvp', AnswerMVP.as_view()),
    path('', views.start, name='start'),
    re_path(r'^login/', LoginAPIView.as_view(), name='user_login'),
    path('login_site/', login_site, name='login_site'),
    path('logout/', logout_user, name='logout'),

]

