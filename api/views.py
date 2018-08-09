from app01 import models
from rest_framework.response import Response
from api import models
# from api.serializers import serializers as api_serializers
from rest_framework.views import APIView


# Create your views here.


# def index(request):
#
    # ORM练习
    # a.查看所有学位课并打印学位课名称以及授课老师
    # degree_course_list = models.DegreeCourse.objects.all()
    # for course in degree_course_list:
    #     for teacher in models.Teacher.objects.all():
    #         print(course.name,teacher.name)
    #
    # print('-'*50)
    #
    #
    #
    # # b.查看所有学位课并打印学位课名称以及学位课的奖学金
    # for course in degree_course_list:
    #     for scholarship in models.Scholarship.objects.all():
    #         print(course.name,scholarship.value)
    #
    # print('-' * 50)
    #
    #
    # # c.展示所有的专题课
    # course_list = models.Course.objects.filter(degree_course__isnull=True)
    # for course in course_list:
    #     print(course.name)
    #
    # print('-' * 50)
    #
    #
    # # d.查看id = 1
    # # 的学位课对应的所有模块名称
    # degree_course = models.DegreeCourse.objects.filter(id = 1).values('name')
    # print(degree_course)
    #
    # print('-' * 50)
    #
    #
    # # e.获取id = 1
    # # 的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses
    # # course_1 = models.Course.objects.filter(degree_course__isnull=True,id = 1)
    # # print(course_1)
    #
    #
    #
    #
    # # f.获取id = 1
    # # 的专题课，并打印该课程相关的所有常见问题
    # course = models.Course.objects.filter(degree_course__isnull=True,id = 1)
    #
    #
    #
    #
    #
    #
    # # g.获取id = 1
    # # 的专题课，并打印该课程相关的课程大纲
    #
    # obj8 = models.Course.objects.filter(degree_course__isnull=True, id=1).values('coursedetail__courseoutline__title')
    # print(obj8)
    # #
    # # h.获取id = 1
    # # 的专题课，并打印该课程相关的所有章节
    # obj8 = models.Course.objects.filter(degree_course__isnull=True, id=1).values('coursechapters__chapter')
    # print(obj8)
    # #
    # # i.获取id = 1
    # # 的专题课，并打印该课程相关的所有课时
    # obj9 = models.Course.objects.filter(degree_course__isnull=True,id=1).values('coursedetail__hours')
    # print(obj9)
    #
    #
    #
    #
    # return HttpResponse('OK')



#查询学位课

# class DegreeCourse(APIView):
#     def get(self,request):
#         res={'code':0}
#         all_degreecourse = models.DegreeCourse.objects.all()
#         ser_obj = api_serializers.DegreeCourseSerializer(all_degreecourse, many=True)
#         res['data'] = ser_obj
#         return Response(res)
#
#
# # 查询专题课
#
# class Course(APIView):
#     def get(self,request):
#         res = {'code': 0}
#         all_course = models.Course.objects.filter(degree_course__isnull=True).all()
#         ser_obj = api_serializers.CourseSerializer(all_course, many=True)
#         res['data'] = ser_obj
#         return Response(res)
#
#
# # 查询课程详情
# class CourseDetail(APIView):
#     def get(self,request):
#         res = {'code': 0}
#         all_coursedetail = models.CourseDetail.objects.all()
#         ser_obj = api_serializers.CourseDetailSerializer(all_coursedetail, many=True)
#         res['data'] = ser_obj
#         return Response(res)






