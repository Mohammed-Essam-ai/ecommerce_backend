from django.urls import path
from .views import *
app_name='cart'


urlpatterns=[
    path('cart-items/',CartItemView.as_view()),
    path('increase-one/',IncreaseOne),
    path('decrease-one/',DecreaseOne),
    path('delete-item/',delete_item),
    path('cart-item-quantity/',get_cart_item_quantity),
]
