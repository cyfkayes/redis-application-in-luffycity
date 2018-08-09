from django.conf.urls import url, include
from s11_luffycity.api.views import course
from s11_luffycity.api.views import shoppingcar


urlpatterns = [
    url(r'course/$', course.CoursesView.as_view()),
    url(r'course/(?P<pk>\d+)/$', course.CourseDetailView.as_view()),
    url(r'shoppingcar/$', shoppingcar.ShoppingCarView.as_view({'post':'create','get':'list','delete':'destroy','put':'update'}))
]