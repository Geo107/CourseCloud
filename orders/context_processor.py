from orders.models import Cart,Wishlist
def cart_count(request):
    if request.user.is_authenticated:
        c_cnt=Cart.objects.filter(student_object=request.user).count()
        w_cnt=Wishlist.objects.filter(student_object=request.user).count()
        return {"cart_count":c_cnt,"wishlist_count":w_cnt}
    else:
        return {"cart_count":0,"wishlist_count":0}
    
