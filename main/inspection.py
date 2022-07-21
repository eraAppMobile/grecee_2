
from main.models import Viqinfo, Viq, Questionpoolnew, Briefcase, Answer, Inspectiontypes, Inspectionsource,\
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
        dictionary_lists = {'vessel': Vessel.objects.all(),
                            'inspectiontype': Inspectiontypes.objects.all(),
                            'sourcename': Inspectionsource.objects.all(),
                            'port': Vettinginfo.objects.exclude(port__isnull=True)
                            }
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
