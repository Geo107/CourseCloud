from django.urls import path
from core.views import *
urlpatterns=[
    path('home',HomeView.as_view(),name='home'),
    path('detail/<int:cid>',DetailsView.as_view(),name='detail'),
    path('addtocart/<int:cid>',AddToCart.as_view(),name="addtocart"),
    path('addtowishlist/<int:cid>',AddToWishlist.as_view(),name="addtowishlist")
]