from venv import create

from django.contrib.auth import logout, authenticate, login
from django.contrib.contenttypes.models import ContentType

from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from PIL import Image as Img
import io
import base64

from .forms import LoginForm
from .models import Viq, Viqinfo, Questionpoolnew, Answer, Image, Briefcase
from .serializers import AnswerMVPSerializer, LoginSerializer


def start(request):
    return render(request, 'main/start.html')

def index(request):
    return render(request, 'main/index.html')


class Question(APIView):

    @classmethod
    def get(cls, request):
        listing = []
        for questions in Viqinfo.objects.all():
            list_chapters = {"qid": questions.qid, "title": questions.title}
            listing.append(list_chapters)
        return Response(listing)


    @classmethod
    def post(cls, request):
        data = request.data
        list_question = []
        for obj in Viq.objects.filter(qid=data['qid']):
            for quest in Questionpoolnew.objects.filter(questionid=obj.objectid):
                list_dict = {
                    'questionid': quest.questionid,
                    'questioncode': quest.questioncode,
                    'question': quest.question,
                    'comment': quest.comment,
                    'categoryid': quest.categoryid,
                    'origin' : quest.origin,
                    'categorynewid': quest.categorynewid,
                }
                list_question.append(list_dict)
        return Response(list_question)


class Answers (APIView):

    @classmethod
    def post(cls, request):
        data = request.data
        name = data.get("briefcase")['InspectorName']
        new_briefcase = Briefcase.objects.create(
            name_case=(data.get("briefcase")['name_case']).capitalize(),
            InspectorName=data.get("briefcase")['InspectorName'],
            InspectionTypes=data.get("briefcase")['InspectionTypes'],
            InspectionSource=data.get("briefcase")['InspectionSource'],
            vessel=data.get("briefcase")['vessel'],
            port=data.get("briefcase")['port'],
            date_in_vessel=data.get("briefcase")['date_in_vessel'],
        )
        for answer in data['answer'].values():
            new_answer = Answer.objects.create(
                briefcase=new_briefcase,
                answer=answer['answer'],  # заменить на ответы с таблицы
                comment=answer['comment'],
                questionid=answer['questionid'],
                question=answer['question'],
                questioncode=answer['questioncode'],
                categoryid=answer['categoryid'],
                categorynewid=answer['categorynewid'],
                origin=answer['origin'],
            )

            # написать цикл если изображений будет приходить несколько
            if 'data_image' in answer:
                for data in answer['data_image'].values():
                    image_answer = base64.b64decode(data)
                    image = Img.open(io.BytesIO(image_answer))
                    image_io = io.BytesIO()
                    image.save(image_io, format='png', name=name, quality=80)
                    image_bd = ContentFile(image_io.getvalue(), name=name)
                    Image.objects.create(
                        answer=new_answer,
                        image=image_bd,
                    )
                continue
            else:
                continue

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(Briefcase).pk,
            object_id=new_briefcase.id,
            object_repr=new_briefcase.name_case,
            action_flag=ADDITION if create else CHANGE)
        return Response({'status': 'Success!'})
        # возвращаем успешный ответ


class AnswerMVP (APIView):
    @classmethod
    def get(cls, request):
        listing = Answer.objects.all()
        result = AnswerMVPSerializer(listing, many=True)  # конвертируем их в json
        if not listing:
            return Response({'status': 'no data!'})
        return Response(result.data)  # возвращаем список примером документов




# class RegistrationAPIView(APIView):
#     """
#     Registers a new user.
#     """
#     permission_classes = [AllowAny]
#     serializer_class = RegistrationSerializer
#
#     def post(self, request):
#         """
#         Creates a new User object.
#         Username, email, and password are required.
#         Returns a JSON web token.
#         """
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(
#             {
#                 'token': serializer.data.get('token', None),
#             },
#             status=status.HTTP_201_CREATED,
#         )


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
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
    return render(request, 'main/start.html')



def logout_user(request):
    logout(request)
    return redirect('start')


def page_not_found(request, exception):
    return render(request, 'main/404.html')


