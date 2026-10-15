from django.urls import path
from . import views
app_name='products'
urlpatterns=[
    path('product/<int:product_id>/',views.ProductView.as_view(),name='product'),
    path('category/<int:x>/',views.ProductListView.as_view(),name='products'),
    path('categories/',views.CategoryListView.as_view(),name='categories'),
    path('',views.ProductListView.as_view()), 
    path('reviews/<int:product_id>',views.ReviewView.as_view()),
    path('brands/',views.get_brands),
    path('styles/',views.get_styles),
    path('happy-reviews/',views.get_happy_reviews),        
]
