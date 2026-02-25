from django.urls import path
from . import views

urlpatterns = [
    path('',                      views.product_list,   name='product_list'),
    path('search/',               views.search,         name='search'),
    path('category/<slug:slug>/', views.category_view,  name='category'),
    path('<slug:slug>/',          views.product_detail, name='product_detail'),
]
