from django.shortcuts import render,redirect
from django.views.generic import ListView
from courses.models import Course,Module,Lesson
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


# Create your views here.
def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.warning(request,"LogIn Required")
            return redirect('login')
    return inner

@method_decorator([signin_required,never_cache],name='dispatch')
class MyCoursesView(ListView):
    template_name='courses/mycourses.html'
    context_object_name='mycourses'

    def get_queryset(self):
        return Course.objects.filter(enrolled_courses__student_object=self.request.user,enrolled_courses__is_paid=True).distinct()

@method_decorator([signin_required,never_cache],name='dispatch')
class LessonView(View):
    def get(self,request,**kwargs):
        course=Course.objects.get(id=kwargs.get('cid'))
        module=Module.objects.filter(course=course).first()
        lesson=Lesson.objects.filter(module=module).first() if 'lesson' not in request.GET else Lesson.objects.get(id=request.GET.get('lesson'))
        return render(request,'courses/viewLessons.html',{"course":course,"lesson":lesson})