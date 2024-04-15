from .models import *
from department.serializers import *
from department.permission import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# this is used to genreate the token RefreshToken
from rest_framework.permissions import IsAuthenticated
from department.permission import CanCreateProjectPermission, Canallocateproject  # Update import path
from .models import CustomUser,Project
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import logout
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render

# this is use to generated token manaually
def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }
# ==========================================-RegisterView-======================================================
# i was not able to import this rendereses file which i have creared
class RegisterView(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            if CustomUser.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'Successful': 'Registration Successful..!',
                 }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# ========================================-LoginView-=========================================================

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        
        # Authenticating user without encrypting the password
        user = authenticate(email=email, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'Successful': 'Login Successful..!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid Credentials..!:['Email' or 'password is not valid']"}, status=status.HTTP_401_UNAUTHORIZED)
        # check
# ===========================================-ChangePassword-======================================================
        
class Changepasswords(APIView):
    # serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data,context=({'user': request.user}))
        
        if serializer.is_valid():
            return Response({'msg':'password changed Done'},status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# done till here
# ===========================================-ResetPassword-1-======================================================
        
# This is used to send email  
class ResetPassword(APIView):

    def post(self, request, format= None):
        serializers = ResetPasswordEmailRequestSerializer(data= request.data)
        if serializers.is_valid():
            return Response({'msg':'password Reset link send. Plase check your email inbox'},status= status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendResetPasswordEmaiView(APIView):
    def post(self, request):
        serializer = SendResetPasswordEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"Successful":"password reset link is sent..!"}, status=status.HTTP_200_OK)

# ============================================-ProjectListView-======================================================   
# admin can view all project create project
        
class ProjectListView(ListAPIView):
    serializer_class = ProjectListSerializer
    queryset = Project.objects.all()
    filter_backends = [filters.DjangoFilterBackend] 

    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return self.queryset  
        else:
            raise PermissionDenied("You do not have permission to view projects.")

# =============================================-projectCreate-=====================================================
# this is use to create a new project

class projectCreateView(APIView):
    
    permission_classes = [CanCreateProjectPermission]
    def post(self, request):
        serializer = ProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ============================================-ProjectCRUDView-=====================================================  
# this is use to do delte and update in any project
    
class ProjectCRUDView(APIView):
    permission_classes = [CanCreateProjectPermission]

    def patch(self, request, id):
        try:
            project = Project.objects.get(pk=id)
            serializer = ProjectCRUDSerializer(project, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"Success": "Changes updated successfully.", "updated_data":serializer.data}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"error": "Project does not exists."},status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            project = Project.objects.get(pk=id)    
            project.delete()
            return Response({"success": "Project deleted successfully."},status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"error": "Project does not exists."},status=status.HTTP_404_NOT_FOUND)


# ===================================================-TotalUserList-=====================================================
# this will show total number of users
class TotalUserList(APIView):
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        total_users = users.count()
        serializer = CustomUserSerializer(users, many=True)
        return Response({'total_users': total_users, 'users': serializer.data})

# =============================================-ProjectAllocationView-====================================================
class ProjectAllocationView(APIView):
    permission_classes = [Canallocateproject]

    def post(self, request):
        serializer = ProjectAllocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Success": "Project allocation successful.", "allocation": serializer.data},
                        status=status.HTTP_201_CREATED)   
# ===========================================-EmployeeAllocation-======================================================
class EmployeeAllocationListView(APIView):
    permission_classes = [Canallocateproject]

    def get(self, request):
        employees = CustomUser.objects.filter(userType="Employee")
        serializer = EmployeeAllocationListSerializer(employees, many=True)
        return Response(serializer.data)
# ===========================================-LogoutView-======================================================
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            print("Refresh token", token)
            token.blacklist()
            LogoutView(request)
            return Response({"success": "Logged out successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# =============================================-TokenRefresh-====================================================
        
class TokenRefreshAPIView(APIView):
    pass 
