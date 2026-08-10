from django.db import models
from accounts.models import User
from django.db.models import Max

# Create your models here.
class Category(models.Model):
    type=models.CharField(max_length=300)

    def __str__(self):
        return self.type

class Course(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    added_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    category=models.ManyToManyField(Category)
    instructor=models.ForeignKey(User,on_delete=models.CASCADE,related_name="instructor_courses")
    image=models.ImageField(upload_to="Course_Images")
    video=models.TextField()
    price=models.DecimalField(max_digits=7,decimal_places=2)
    is_free=models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Module(models.Model):
    title=models.CharField(max_length=500)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="modules")
    order_number=models.PositiveIntegerField()

    def save(self, *args,**kwargs):
        if not self.order_number:
            max_order=Module.objects.filter(course=self.course).aggregate(max=Max('order_number')).get('max') or 0
            self.order_number=max_order+1
        return super().save(*args,**kwargs)

    class Meta:
        ordering=['order_number']

    def __str__(self):
        return f"{self.order_number} {self.title}"

class Lesson(models.Model):
    title=models.CharField(max_length=500)
    module=models.ForeignKey(Module,on_delete=models.CASCADE,related_name="lessons")
    video=models.TextField()
    order_number=models.PositiveIntegerField()

    def save(self, *args,**kwargs):
        if not self.order_number:
            max_order=Lesson.objects.filter(module=self.module).aggregate(max=Max('order_number')).get('max') or 0
            self.order_number=max_order+1
        super().save(*args,**kwargs)

    class Meta:
        ordering=['order_number']

    def __str__(self):
            return f"{self.order_number}.  {self.title}"