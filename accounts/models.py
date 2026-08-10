from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class User(AbstractUser):
    ROLE_OPTIONS=[
        ("Student","Student"),
        ("Instructor","Instructor")
    ]

    role=models.CharField(max_length=500,default="Student",choices=ROLE_OPTIONS)

    def __str__(self):
        return self.username

class InstructorProfile(models.Model):
    about=models.TextField(blank=True)
    expertise=models.CharField(max_length=500,blank=True)
    instructor=models.OneToOneField(User,on_delete=models.CASCADE,related_name="instructor_profile")
    image=models.ImageField(upload_to="Instructor_Images",default="instructor_default.jpeg")

    def __str__(self):
            return self.instructor.username

@receiver(post_save,sender=User)
def createInstructorProfile(sender,instance,**kwargs):
    if instance.role=="Instructor":
         InstructorProfile.objects.get_or_create(instructor=instance)