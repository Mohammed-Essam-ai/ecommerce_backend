from django.urls import path
from .views import *
app_name='orders'

urlpatterns=[
    path('',OrderView.as_view(),name='orders'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('<int:order_id>/confirm/',ConfirmOrderView.as_view(),name='confirm-order'),
    path('<int:order_id>/cancel/',CancelOrderView.as_view(),name='cancel-order'),
]