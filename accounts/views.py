from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView
from accounts.forms import *
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login,logout
from django.views import View
# Create your views here.

class StudentSignUpView(CreateView):
    template_name='accounts/signup.html'
    form_class=SignUpForm
    success_url=reverse_lazy('acclogin')

class InstructorSignUpView(CreateView):
    template_name='accounts/Isignup.html'
    form_class=SignUpForm
    success_url=reverse_lazy('acclogin')

    def form_valid(self, form):
        form.instance.role="Instructor"
        form.instance.is_superuser=True
        form.instance.is_staff=True
        return super().form_valid(form)

class LogInView(FormView):
    template_name='accounts/login.html'
    form_class=LogInForm

    def post(self,request):
        form_data=LogInForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request,user)
                if user.role=="Student":
                    return redirect('home')
                elif user.role=="Instructor":
                    return redirect(reverse('admin:index'))
            else:
                return redirect('signin')
        return render(request,'accounts/signin.html',{"form":form_data})

class LogOutView(View):
    def get(self,request):
        logout(request)
        return redirect('acclogin')