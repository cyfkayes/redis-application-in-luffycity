from api import models
from rest_framework import serializers


#课程类的序列化

# class DegreeCourseSerializer(serializers.Serializer):
#     class Meta:
#         model = models.DegreeCourse
#         fields = '__all__'
#
# class CourseSerializer(serializers.Serializer):
#     class Meta:
#         model = models.Course
#         fields = "__all__"
# class CourseDetailSerializer(serializers.Serializer):
#     class Meta:
#         model = models.CourseDetail
#         fields = '__all__'
class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class CourseModelSerializer(serializers.ModelSerializer):
    #source帮助做跨表查询--->ModelSeriliazer  获取只想要的字段，source='表名小写'
    level_name = serializers.CharField(source = 'get_level_display')
    hours = serializers.CharField(source='coursedetail.hours')
    course_slogan = serializers.CharField(source='coursedetail.course_slogan')

    recommend_courses = serializers.SerializerMethodField()

    class Meta:
        models = models.Course
        fields = ['id','name','level','hours','course_slogan','recommend_courses']

    def get_recommend_courses(self,row):
        recommend_list = row.coursedetail.recommend_courses.all()
        return [{'id':item.id,'name':item.name} for item in recommend_list]