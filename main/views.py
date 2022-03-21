from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from PIL import Image as Img
import io
import base64


from .models import Viq, Viqinfo, Questionpoolnew, Answer, Image
from .serializers import AnswerMVPSerializer, LoginSerializer


class Question(APIView):

    def get(self, request):
        listing = []
        for questions in Viqinfo.objects.all():
            list_cat = {"qid": questions.qid, "title": questions.title}
            listing.append(list_cat)
        return Response(listing)

    def post(self, request):
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
                    'categorynewid': quest.categorynewid
                }
                list_question.append(list_dict)
        return Response(list_question)


class Answers (APIView):
    # переработать вопросы ( создать портфель вопросов, может включать разное кол-во ответов)
    def post(self, request):
        data = request.data
        # try:
        #     if Answer.objects.filter():

        new_answer = Answer.objects.create(
            InspectorName=data.get("answer")['InspectorName'],
            answer=data.get("answer")['answer'],
            comment=data.get("answer")['comment'],
            questionid=data.get("answer")['questionid'],
            questioncode=data.get("answer")['questioncode'],
            categoryid=data.get("answer")['categoryid'],
            categorynewid=data.get("answer")['categorynewid'],
            origin=data.get("answer")['origin'],
            vessel=data.get("answer")['vessel'],
            port=data.get("answer")['port'],
            InspectionTypes=data.get("answer")['InspectionTypes'],
            InspectionSource=data.get("answer")['InspectionSource'],
            date_in_vessel=data.get("answer")['date_in_vessel'],
        )
        # написать цикл если изображений будет приходить несколько
        if data['data_image']:
            name = data.get("answer")['InspectorName']
            for data in data['data_image'].values():
                image_answer = base64.b64decode(data)
                image = Img.open(io.BytesIO(image_answer))
                image_io = io.BytesIO()
                image.save(image_io, format='png', name=name, quality=80)
                image_bd = ContentFile(image_io.getvalue(), name=name)
                Image.objects.create(
                    answer=new_answer,
                    image=image_bd,
                )
            return Response({'status': 'Success!'})  # возвращаем успешный ответ


class AnswerMVP (APIView):
    def get(self, request):
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
