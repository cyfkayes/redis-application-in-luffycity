
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from api.utils.response import BaseResponse
from api import models

from rest_framework.pagination import PageNumberPagination
from api.serializers.course import CourseModelSerializer
from rest_framework.response import Response



class CoursesView(APIView):

    def get(self, request, *args, **kwargs):

        ret = BaseResponse()
        try:
            #get data from db
            queryset = models.Course.objects.all()
            #分页
            page = PageNumberPagination()
            course_list = page.paginate_queryset(queryset, request, self)
            #分页后的结果执行序列化
            ser = CourseModelSerializer(instance=course_list, many=True)

            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = 'failed to get data'
        return Response(ret.dict)

class CourseDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        response = {'code':1000, 'data':None, 'error':None}
        try:
            course = models.Course.objects.get(id=pk)
            ser = CourseModelSerializer(instance=course)
            response['data'] = ser.data
        except Exception as e:
            response['code'] = 500
            response['error'] = 'failed to get data'
        return Response(response)