
from django.urls import path,include
from django import views
from department.views import *
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),
    path('Project/', ProjectViewSet.as_view(), name='project'),
    path('Changepasswords/', UserChangePasswordView.as_view(), name='changepass'),
    #ResetPassword
    path('ResetPassword/', ResetPassword.as_view(), name='resetPassword'),
    
]
