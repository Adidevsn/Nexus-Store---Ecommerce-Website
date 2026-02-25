from django.urls import path
from . import views

urlpatterns = [
    path('',                 views.cart_detail,  name='cart'),
    path('add/<int:id>/',    views.cart_add,     name='cart_add'),
    path('remove/<int:id>/', views.cart_remove,  name='cart_remove'),
    path('update/<int:id>/', views.cart_update,  name='cart_update'),
    path('clear/',           views.cart_clear,   name='cart_clear'),
]
