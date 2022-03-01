from django.urls import path
from .views import *
from product import views

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', login.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', Logout.as_view()),
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search/', views.search),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
    path('checkout/', views.checkout),
    path('orders/', views.OrdersList.as_view()),
]