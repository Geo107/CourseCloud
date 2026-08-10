from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView
from courses.models import Course
from orders.models import Order
from django.views import View
from orders.models import Cart,Wishlist
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.
def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"LogIn Required")
            return redirect('acclogin')
    return inner

@method_decorator([signin_required,never_cache],name='dispatch')
class HomeView(ListView):
    template_name='core/home.html'
    queryset=Course.objects.all()
    context_object_name='courses'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        purchased_courses=Order.objects.filter(student_object=self.request.user,is_paid=True).values_list('course_object',flat=True)
        context["purchased_courses"]=purchased_courses
        return context

@method_decorator([signin_required,never_cache],name='dispatch')
class DetailsView(DetailView):
    template_name='core/detail.html'
    pk_url_kwarg='cid'
    queryset=Course.objects.all()
    context_object_name='course'

@method_decorator([signin_required,never_cache],name='dispatch')
class AddToCart(View):
    def get(self,request,**kwargs):
        (objects,created)=Cart.objects.get_or_create(student_object=request.user,course_object=Course.objects.get(id=kwargs.get('cid')))
        if created:
            return redirect('home')
        else:
            messages.warning(request,"Course already added to cart!")
            return redirect('home')

@method_decorator([signin_required,never_cache],name='dispatch')
class AddToWishlist(View):
    def get(self,request,**kwargs):
        (objects,created)=Wishlist.objects.get_or_create(student_object=request.user,course_object=Course.objects.get(id=kwargs.get('cid')))
        if created:
            return redirect('home')
        else:
            messages.warning(request,"Course already added to wishlist!")
            return redirect('home')