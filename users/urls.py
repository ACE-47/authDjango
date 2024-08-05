from django.urls import path
from .views import (CustomTokenObtainPairView,
                    CustomTokenRefreshView,
                    CustomTokenVerifyView,
                    LogOutView)


urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogOutView.as_view()),

]
