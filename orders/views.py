from django.shortcuts import render,redirect
from orders.models import *
from django.views.generic import ListView
from django.views import View
from courses.models import Course
from django.contrib import messages
from orders.models import Order,Cart,Wishlist
import razorpay
from decouple import config
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
# Create your views here.
RAZORPAY_KEY=config('RAZORPAY_KEY')
RAZORPAY_SECRET_KEY=config('RAZORPAY_SECRET_KEY')

def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.warning(request,"LogIn Required")
            return redirect('login')
    return inner

@method_decorator([signin_required,never_cache],name='dispatch')
class WishlistView(ListView):
    template_name='orders/wishlist.html'
    context_object_name='wishlist_courses'

    def get_queryset(self):
        return Wishlist.objects.filter(student_object=self.request.user)

@method_decorator([signin_required,never_cache],name='dispatch')
class AddToWishlist(View):
    def get(self,request,**kwargs):
        course=Course.objects.get(id=kwargs.get('tid'))
        (object,created)=Wishlist.objects.get_or_create(trail_object=course,hiker_object=request.user)
        if created:
            return redirect('home')
        else:
            messages.success(request,"Trail already added to Wishlist")
            return redirect('home')

@method_decorator([signin_required,never_cache],name='dispatch')
class DeleteWishlist(View):
    def get(self,request,**kwargs):
        Wishlist.objects.get(student_object=request.user,course_object=kwargs.get('cid')).delete()
        return redirect('wishlist')

@method_decorator([signin_required,never_cache],name='dispatch')
class CartView(ListView):
    def get(self,request):
        data=Cart.objects.filter(student_object=self.request.user)
        total=0
        count=data.count()
        for i in data:
            total+=i.course_object.price
        return render(request,'orders/cart.html',{"cart":data,"count":count,"total":total})
    
@method_decorator([signin_required,never_cache],name='dispatch')
class DeleteFromCart(View):
    def get(self,request,**kwargs):
        Cart.objects.get(id=kwargs.get('cid'),student_object=request.user).delete()
        return redirect('cart')

@method_decorator([signin_required,never_cache],name='dispatch')
class PlaceOrder(View):
    def get(self,request):
        cart_total=0
        qs=Cart.objects.filter(student_object=request.user)
        for i in qs:
            cart_total+=i.course_object.price
        order=Order.objects.create(student_object=request.user,total=cart_total)
        for i in qs:
            order.course_object.add(i.course_object)
        qs.delete()
        if cart_total>0:
            client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET_KEY))
            data = { "amount": int(cart_total*100), "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)
            order.razr_pay_order_id=payment.get('id')
            order.save()
            context={
                "key":RAZORPAY_KEY,
                "razr_id":payment.get('id'),
                "amount":int(cart_total*100)
            }
            return render(request,'orders/payment.html',{"data":context})
        elif cart_total==0:
            order.is_paid=True
            order.save()
            return redirect('home')
        return redirect('home')

@method_decorator([csrf_exempt],name="dispatch")
class PaymentVerify(View):
    def post(self,request):
        client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET_KEY))
        try:
            client.utility.verify_payment_signature(request.POST)
            order=Order.objects.get(razr_pay_order_id=request.POST.get('razorpay_order_id'))
            order.is_paid=True
            order.save()
        except Exception as e:
            print(e)
            print("Failed")
        return redirect('home')