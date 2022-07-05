
from django.urls import path, re_path

from . import views
from .inspection import QuestionChapters, Answers,  InfoBriefcase
from .views import LoginAPIView, logout_user, login_site, AnswerMVP, Chapters, Vessel

urlpatterns = [

    path('api/question', QuestionChapters.as_view()),
    path('api/chapters', Chapters.as_view()),
    path('api/infobiefcase', InfoBriefcase.as_view()),
    path('api/answer', Answers.as_view()),
    path('api/answer_questions', AnswerMVP.as_view()),
    path('', views.start, name='start'),
    re_path(r'^login/', LoginAPIView.as_view(), name='user_login'),
    path('login_site/', login_site, name='login_site'),
    path('logout/', logout_user, name='logout'),
    path('index', views.index, name='index'),
    path('index_web', views.index_web, name='index_web'),

    path('api/test_vessel', Vessel.as_view())


]

