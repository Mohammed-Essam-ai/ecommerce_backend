from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import *
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'

urlpatterns=[
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    # ---------------------------------
    path('register/', RegiseterView.as_view()),
    path('user/update/', UpdateUserrView.as_view()),
    path('profile/', ProfileView.as_view()),
]

'''
{
    "user": {
        "username": "mahmoud",
        "email": "mahmoudd@gmail.com"
    },
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4ODAxMjgzOSwiaWF0IjoxNzg3OTI2NDM5LCJqdGkiOiJiNjNhMWZmMGJmMjQ0ZjhkOTc0ZTBhOGE4MjU3YTY0NCIsInVzZXJfaWQiOiIzIn0.oV4z02tc6kki54hKYGnS7WnmjnIxDJF4Sys-Ds8MdeQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg3OTI2NzM5LCJpYXQiOjE3ODc5MjY0MzksImp0aSI6IjlmOTA1ZGE2MTY0OTQ3ZTY5ZWE4ODI0NjNlMGRhNGRjIiwidXNlcl9pZCI6IjMifQ.l-7N9TPltK8jrlWtKaI4RROpIZ_UVN2begMNG8Ua0xM"
}

'''