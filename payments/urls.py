from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/<int:order_id>/complete/', views.complete_payment, name='complete_payment'),
    path('my-courses/', views.my_courses, name='my_courses'),
]
