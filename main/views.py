from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Viq, Viqinfo, Questionpoolnew, Answer
from .serializers import AnswerMVPSerializer, RegistrationSerializer, LoginSerializer


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

    def post(self, request):
        data = request.data
        # try:
        #     if Answer.objects.filter():

        Answer.objects.create(
            InspectorName=data.get("answer")['InspectorName'],
            ansver=data.get("answer")['ansver'],
            comment=data.get("answer")['InspectorName'],
            questionid=data.get("answer")['comment'],
            questioncode=data.get("answer")['questioncode'],
            categoryid=data.get("answer")['categoryid'],
            categorynewid=data.get("answer")['categorynewid'],
            origin=data.get("answer")['origin']
        )

        return Response({'status': 'Succes!'})  # возвращаем успешний ответ


class AnswerMVP (APIView):
    def get(self, request):
        listing = Answer.objects.all()
        result = AnswerMVPSerializer(listing, many=True)  # конвертируем их в json
        return Response(result.data)  # возвращаем список примером документов




class RegistrationAPIView(APIView):
    """
    Registers a new user.
    """
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )


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
