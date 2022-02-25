# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
#
# from .models import Viq, Viqinfo, Questionpoolnew
# from .serializers import ListCategorySerializer
#
#
#
# class AddListCategory(APIView):
#     def get(self, request):
#         list_cat = {}
#         for questions in Viqinfo.objects.all():
#             list_cat['qid'] = questions.qid
#             list_cat['title'] = questions.title
#         result_list = ListCategorySerializer(list_cat, many=True)
#         return Response(result_list.data)
#
#
#     def post(self, request):
#         data = request.data
#         list_question = {}
#         for obj in Viq.objects.filter(qid=data['id']):
#             for quest in Questionpoolnew.objects.filter(questionid=obj.objectid):
#                 list_question['questionid'] = quest.questionid
#                 list_question['question'] = quest.question
#         result_list = ListQuestionSerializer(list_question, many=True)
#         return Response(result_list.data)
#
#
#
#
# #функция создания словаря из таблицы VIQinfo ( Qid : title)
# # def list_category():
# #     list_cat = {}
# #     for questions in Viqinfo.objects.all():
# #         list_cat[questions.qid] = questions.title
# #     return list_cat
# #
# #
# # # список токенов по id категории(Qid) для вопросов для следующей таблицы qustionpoonew
# # def parent_id(id):
# #     list_obj = []
# #     for obj in Viq.objects.filter(qid=id):
# #         list_obj.append(obj.objectid)
# #
# #     questin = []
# #     for tok in list_obj:
# #         for quest in Questionpoolnew.objects.filter(questionid=tok):
# #             print(quest.question)
# #             if quest.question not in questin:
# #                 questin.append(quest.question)
# #     print(questin)
# #     print(len(questin))
# #
# #
# #
# #
# # def questions(token):
# #     pass
#
#
