import base64
from venv import create

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.views import APIView
from PIL import Image as Img
import io

from main.models import Viqinfo, Viq, Questionpoolnew, Briefcase, Answer, Image, Inspectiontypes, Inspectionsource,\
    Vessel, Vettinginfo
from main.serializers import AnswerMVPSerializer, ChaptersSerializer, BriefcaseSerializer, QuestionListSerializer, \
    BriefCaseDataBaseSerializer


class GetDataBase:
    """
    Класс для получения ответов, глав вопросов, информации для создания брифкейса,
    получение вопросов выбранной главы
    """

    # получение ответов
    def get_answers(self):
        listing = Answer.objects.all()
        result = AnswerMVPSerializer(listing, many=True)
        return result

    # отправка информации для создания брифкейса,
    # получение списка портов, кораблей, типа инспекции, источника инспекции
    def get_info_briefcase(self):
        dictionary_lists = {}
        dictionary_lists['vessel'] = Vessel.objects.all()
        dictionary_lists['inspectiontype'] = Inspectiontypes.objects.all()
        dictionary_lists['sourcename'] = Inspectionsource.objects.all()
        dictionary_lists['port'] = Vettinginfo.objects.exclude(port__isnull=True)
        result = BriefcaseSerializer(dictionary_lists)
        return result

    # получение глав вопросов
    def get_chapters(self):
        listing = Viqinfo.objects.all()
        result = ChaptersSerializer(listing, many=True)

        return result

    #получение вопросов выбранной категории, требуется qid
    #!!! разобраться с нулевыми значениями!!!!
    def get_question_chapters(self, data):
        list_object_question = []
        dict_question_object_for_serializer = {}
        for obj in Viq.objects.filter(qid=data):
            list_object_question.append(Questionpoolnew.objects.filter(questionid=obj.objectid).first())
        dict_question_object_for_serializer['question'] = list_object_question
        result = QuestionListSerializer(dict_question_object_for_serializer)

        return result


class BriefcaseBD:
    """
    Для работы с брифкейсами и ответами на вопрос
    """
    def save_briefcase(self):
        pass

    def get_briefcase(self):
        queryset = Briefcase.objects.all()
        data = BriefCaseDataBaseSerializer(queryset, many=True)
        return data

class Answers (APIView):
    """ создание и сохранение заполненного брифкейса клиентом"""
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
                briefcase_answer=new_briefcase,
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
                    image_bd = ContentFile(image.getvalue(), name=name)
                    Image.objects.create(
                        answer_image=new_answer,
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

