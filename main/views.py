from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import LoginForm
from .inspection import GetDataBase, BriefcaseBD
from .serializers import LoginSerializer, BriefCaseDataBaseSerializer


class BriefCase(APIView):
    """
    Класс для просмотра сохраненных брифкейсов, вместе с ответами и фотографиями (GET),
    и POST запрос для создания брифкейсов вместе с ответами и фотографиями если они есть
    """

    def get(self, request):
        result = BriefcaseBD().get_briefcase()
        return Response(result.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        result = BriefCaseDataBaseSerializer(data=data, many=True)
        if result.is_valid(raise_exception=True):
            result.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Question(APIView):
    """
    получение вопросов выбранной категории, требуется qid
    """
    def get(self, request):
        result = GetDataBase().get_question_chapters(data=request.GET.get("qid"))
        if not result.data:
            return Response({'status': 'no data'})
        return Response(result.data.values())


class AnswerMVP(APIView):

    def get(self, request):
        result = GetDataBase().get_answers()
        if not result:
            return Response({'status': 'no data!'})
        return Response(result.data, status=status.HTTP_200_OK)


class Chapters(APIView):
    """Список категорий"""

    def get(self, request):
        result = GetDataBase().get_chapters()
        if not result:
            return Response({'status': 'no data!'}, status=status.HTTP_200_OK)
        return Response(result.data, status=status.HTTP_200_OK)


class InfoBriefCase(APIView):
    """Список информации для создания брифкейса (порт. название корабля, тип инспеции, источник инспекции"""

    def get(self, request):
        result = GetDataBase().get_info_briefcase()
        if not result:
            return Response({'status': 'no data!'})
        return Response(result.data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def get(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """

        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


def login_site(request):
    if request.user.is_authenticated:
        return redirect(reverse('start'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user:
                redirect_url = reverse('start')
                login(request, user)
                return redirect(redirect_url)
        else:
            error = 'Something went wrong...'
            return render(request, 'main/start.html', {'error': error})
    return render(request, 'main/start.html')



def logout_user(request):
    logout(request)
    return redirect('start')


def page_not_found(request, exception):
    return render(request, 'main/404.html')


def start(request):
    return render(request, 'main/start.html')


def index(request):
    return render(request, 'main/index.html')


def index_web(request):
    return render(request, 'main/index_web.html')
