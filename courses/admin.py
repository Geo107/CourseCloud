from django.contrib import admin
from courses.models import *
from accounts.models import *
from django.contrib.admin import ModelAdmin,TabularInline
# Register your models here.

admin.site.register(User)

class InstructorProfileModelAdmin(ModelAdmin):
    model=InstructorProfile
    exclude=('instructor',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(instructor=request.user)

    def has_add_permission(self, request):
        return False

admin.site.register(InstructorProfile,InstructorProfileModelAdmin)

admin.site.register(Category)

class CourseModelAdmin(ModelAdmin):
    model=Course
    exclude=("instructor",)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.instructor=request.user
        return super().save_model(request, obj, form, change)

admin.site.register(Course)

class LessonInline(TabularInline):
    model=Lesson
    extra=1
    exclude=('order_number',)

class ModuleModelAdmin(ModelAdmin):
    exclude=("order_number",)
    inlines=[LessonInline]

admin.site.register(Module,ModuleModelAdmin)
