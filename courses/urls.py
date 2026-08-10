from django.urls import path
from courses.views import *

urlpatterns=[
    path('mytrails',MyCoursesView.as_view(),name="mycourses"),
    path('lessons/<int:cid>',LessonView.as_view(),name='mylessons')
]