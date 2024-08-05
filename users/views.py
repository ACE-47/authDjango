from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # for create 
    TokenRefreshView, # for refresh 
    TokenVerifyView # verify if access token is still valid
)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs) :
        response =  super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            response.set_cookie(
                'access',
                access_token,
                max_age = settings.AUTH_COOCKIE_ACCESS_MAX_AGE,
                path = settings.AUTH_COOCKIE_PATH,
                httponly = settings.AUTH_COOCKIE_HTTP_ONLY,
                samesite = settings.AUTH_COOCKIE_SAMESITE,
                secure = settings.AUTH_COOKIE_SECURE
            )
            
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age = settings.AUTH_COOCKIE_REFRESH_MAX_AGE,
                path = settings.AUTH_COOCKIE_PATH,
                httponly = settings.AUTH_COOCKIE_HTTP_ONLY,
                samesite = settings.AUTH_COOCKIE_SAMESITE,
                secure = settings.AUTH_COOKIE_SECURE
            )
            
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs) :
        
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token:
            request.data['refresh'] = refresh_token
                
        respose = super().post(request, *args, **kwargs)
        if respose.status_code == 200 :
            access_token = respose.data.get('access')
            
            respose.set_cookie(
                'access',
                access_token,
                max_age = settings.AUTH_COOCKIE_ACCESS_MAX_AGE,
                path = settings.AUTH_COOCKIE_PATH,
                httponly = settings.AUTH_COOCKIE_HTTP_ONLY,
                samesite = settings.AUTH_COOCKIE_SAMESITE,
                secure = settings.AUTH_COOKIE_SECURE
            )
        
        return respose
    
    
class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs) :
        access_token = request.COOKIES.get('access')
        
        if access_token:
            request.data['token'] = access_token
        
        return super().post(request, *args, **kwargs)
        

class LogOutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        
        return response