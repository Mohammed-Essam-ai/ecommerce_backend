from django.urls import path
from . import views
app_name='products'
urlpatterns=[
    path('product/<int:x>/',views.ProductView.as_view(),name='product'),
    path('products/<int:x>/',views.ProductListView.as_view(),name='products'),
    path('categories/',views.CategoryListView.as_view(),name='categories'),
    path('creteorder/',views.CreateOrderView.as_view(),name='creteorder'),
    path('orders/',views.OrderListView.as_view(),name='orders'),
]

