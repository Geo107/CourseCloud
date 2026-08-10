from django.urls import path
from orders.views import *

urlpatterns=[
    path('wishlist',WishlistView.as_view(),name="wishlist"),
    path('remwishlist/<int:cid>',DeleteWishlist.as_view(),name="remwishlist"),
    path('remcart/<int:cid>',DeleteFromCart.as_view(),name="remcart"),
    path('cart',CartView.as_view(),name="cart"),
    path('checkout',PlaceOrder.as_view(),name='checkout'),
    path('payment-verify',PaymentVerify.as_view(),name='payment-verify')
]