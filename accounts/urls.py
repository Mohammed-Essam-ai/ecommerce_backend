from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import RegiseterView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'

urlpatterns=[
    path('register/',RegiseterView.as_view(),name='register'),
    path('login/',obtain_auth_token,name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('changepassword/',auth_views.PasswordChangeView.as_view(template_name='acounts/changepassword.html',success_url='changepassworddone'),name='changepassword'),
    path('changepassworddone/',auth_views.PasswordChangeDoneView.as_view(template_name='acounts/changepassworddone.html'),name='changepassworddone'),
    path('editprofile/',views.EditProfileView.as_view(),name='editprofile')
]

