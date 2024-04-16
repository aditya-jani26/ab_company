
from django.urls import path,include
from department.views import *
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
)

urlpatterns = [

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),

    path('register/', RegisterView.as_view(), name='register'),
    path('Changepasswords/', Changepasswords.as_view(), name='Changepasswords'),
    path('ResetPassword/', ResetPassword.as_view(), name='ResetPassword'),
    path('sendpassword/',SendResetPasswordEmaiView.as_view(), name='sendpassword'),

    path('login/', LoginView.as_view(), name='login'),

    path('ProjectList/', ProjectList.as_view(), name='ProjectList-list'),
    path('projectCreateView/', projectCreateView.as_view(), name='projectCreateView'),
    path('ProjectCRUDView/', ProjectCRUDView.as_view(), name='ProjectCRUDView'),
    path('ProjectAllocationView/', ProjectAllocationView.as_view(), name='ProjectAllocationView'),

    path('EmployeeAllocation/', EmployeeAllocationListView.as_view(), name='EmployeeAllocation'),
    path('TotalUserList/',TotalUserList.as_view(), name='TotalUserList'),

    path('LogoutView/',LogoutView.as_view(), name='LogoutView'),

]
