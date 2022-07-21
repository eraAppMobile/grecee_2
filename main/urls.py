from django.urls import path, re_path

from .views import LoginAPIView, logout_user, login_site, AnswerMVP, Chapters, InfoBriefCase, Question, BriefCase, \
    start, index, index_web

urlpatterns = [

    path('api/question', Question.as_view()),
    path('api/chapters/', Chapters.as_view()),
    path('api/infobiefcase', InfoBriefCase.as_view()),
    path('api/answer_questions', AnswerMVP.as_view()),
    path('api/briefcase', BriefCase.as_view()),
    re_path(r'^login/', LoginAPIView.as_view(), name='user_login'),

    path('', start, name='start'),
    path('login_site/', login_site, name='login_site'),
    path('logout/', logout_user, name='logout'),
    path('index', index, name='index'),
    path('index_web', index_web, name='index_web'),

]
