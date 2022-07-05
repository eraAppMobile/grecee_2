import base64
from venv import create

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from PIL import Image as Img
import io

from main.models import Viqinfo, Viq, Questionpoolnew, Briefcase, Answer, Image, Inspectiontypes, Inspectionsource,\
    Vessel, Vettinginfo
from main.serializers import AnswerMVPSerializer, ChaptersSerializer, VesselSerializer, BriefcaseSerializer


class InfoBriefcase(APIView):
    """
    Информация для селектов при создании и заполнении брифкейса
    """
    def get(self, request):

        #список судов
        vessel = []
        for obj_vessel in Vessel.objects.all():
            vessel.append(obj_vessel.vesselname.strip())

        #список вида инспеkции
        inspection_type =[]
        for obj_inspectiontype in Inspectiontypes.objects.all():
            inspection_type.append(obj_inspectiontype.inspectiontype)

        # список ресурсов инспекции
        instection_source = []
        for obj_inspectionsource in Inspectionsource.objects.all():
            instection_source.append(obj_inspectionsource.sourcename)

        #список портов с сортировкой повторяющихся
        port_sorted = []
        for obj_ports in Vettinginfo.objects.all():
            if obj_ports.port != None:
                port_symbol_lower=obj_ports.port.lower()
                if port_symbol_lower not in port_sorted:
                    port_sorted.append(port_symbol_lower)
        ports = []
        for el in port_sorted:
            p=el.title()
            ports.append(p)
        listing = {'vessel':vessel, "port":ports , "inspection_type":inspection_type,
                        "inspecstion_source":instection_source}

        return Response(listing)


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
        listing = {}
        listing['vessel'] = Vessel.objects.all()
        listing['inspectiontype'] = Inspectiontypes.objects.all()
        listing['sourcename'] = Inspectionsource.objects.all()
        listing['port'] = Vettinginfo.objects.exclude(port__isnull=True)
        result = BriefcaseSerializer(listing)
        return result

    # получение глав вопросов
    def get_chapters(self):
        listing = Viqinfo.objects.all()
        result = ChaptersSerializer(listing, many=True)

        return result

    #получение вопросов выбранной категории, требуется qid
    def get_question_chapters(self):
        pass


class BriefcaseBD:
    """
    Для работы с брифкейсами и ответами на вопрос
    """
    def save_briefcase(self):
        pass


class QuestionChapters(APIView):
    """Список вопросов категории. ДЛя получения необходим qid"""

    def post(self, request):
        data = request.data
        list_question = []
        # question_ids = Viq.objects.filter(qid=data['qid']).values_list('objectid')
        for obj in Viq.objects.filter(qid=data['qid']):
            for quest in Questionpoolnew.objects.filter(questionid=obj.objectid):
                list_dict = {
                    'questionid': quest.questionid,
                    'questioncode': quest.questioncode,
                    'question': quest.question,
                    'comment': quest.comment,
                    'categoryid': quest.categoryid,
                    'origin': quest.origin,
                    'categorynewid': quest.categorynewid,
                }
                list_question.append(list_dict)
        return Response(list_question)


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

