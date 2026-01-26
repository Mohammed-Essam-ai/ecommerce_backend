from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
# from .forms import SignupForm ,EditProfileForm,EditUserForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import RegisterSerializer ,EditProfileSerializer
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token

class RegiseterView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response(status=201)
        return Response(serializer.errors,status=400)
    
class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request):
        Token.objects.filter(user=request.user).delete()
        return Response({'message':'you have logged out'})    
    
class EditProfileView(RetrieveUpdateAPIView):
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
