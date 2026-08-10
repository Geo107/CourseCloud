from django.db import models
from accounts.models import User
from courses.models import Course
# Create your models here.
class Cart(models.Model):
    course_object=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_cart_object")
    student_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="student_cart_object")
    added_at=models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    course_object=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_wishlist_object")
    student_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="student_wishlist_object")
    added_at=models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    razr_pay_order_id=models.CharField(max_length=500,null=True)
    course_object=models.ManyToManyField(Course,related_name="enrolled_courses")
    student_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="purchase")
    is_paid=models.BooleanField(default=False)
    total=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)