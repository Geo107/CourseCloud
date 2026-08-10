from django.urls import path
from accounts.views import *

urlpatterns=[
    path('signup',StudentSignUpView.as_view(),name="accsignup"),
    path('login',LogInView.as_view(),name="acclogin"),
    path('logout',LogOutView.as_view(),name="acclogout"),
    path('isignup',InstructorSignUpView.as_view(),name="isignup"),
]