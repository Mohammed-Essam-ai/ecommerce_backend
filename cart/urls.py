from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('cart-items/', CartItemView.as_view(), name='cart-items'),
    path('increase-one/', IncreaseOne, name='increase-one'),
    path('decrease-one/', DecreaseOne, name='decrease-one'),
    path('delete-item/', delete_item, name='delete-item'),
    path('cart-item-quantity/', get_cart_item_quantity, name='cart-item-quantity'),
]