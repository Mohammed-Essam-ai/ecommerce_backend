from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import *
from rest_framework.response import Response 
from rest_framework_simplejwt.tokens import RefreshToken


class RegiseterView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=400)

class UpdateUserrView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self,request):
        user = request.user
        serializer=UpdateUserSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            user=serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors,status=400)   

    

class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        profile=Profile.objects.get(user=request.user)
        serializer=ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self,request):
        profile=Profile.objects.get(user=request.user)
        serializer=ProfileSerializer(profile,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

