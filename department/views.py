from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# this is used to genreate the token RefreshToken
from rest_framework.permissions import IsAuthenticated
from department.permission import CanCreateProjectPermission  # Update import path
from department.serializers import *
from .models import CustomUser,Project
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import *
from rest_framework_simplejwt.views import TokenRefreshView
# this is use to generated token manaually
def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }
# i was not able to import this rendereses file which i have creared
class RegisterView(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            if CustomUser.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()
            refresh = get_token_for_user(user)
            return Response({
                'Successful': 'Registration Successful..!',
                 }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        print('email',email)
        password = serializer.validated_data.get('password')
        print('password',password)

        user = authenticate(request, email=email, password=password)
        print('email',email,"password",password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'Successful': 'Login Successful..!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid Credentials..!:['Email' or 'password is not valid']"}, status=status.HTTP_401_UNAUTHORIZED)
            
class CustomUserViewSet(APIView):
    
    serializer_class = CustomUserSerializer

    def create(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            queryset = CustomUser.objects.all()
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 # Make sure to import the serializer

class ProjectViewSet(APIView):
    serializer_class = ProjectSerializer  # Use the correct serializer class name
    permission_classes = [CanCreateProjectPermission]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():   
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserChangePasswordView(APIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None , *args, **kwargs):
        serializer_class = ChangePasswordSerializer(data=request.data)
        context=({'user': request.user})
        if serializers.is_valid(raise_exception=True):
            return Response({'msg':'password changed succeddfully'},status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
# this is used to send email with the help of email link
class ResetPassword(APIView):

    def post(self, request, format= None):
        serializers = ResetPasswordEmailRequestSerializer(data= request.data)
        if serializers.is_valid(raise_exceptions=True):
            return Response({'msg':'password Reset link send. Plase check your email inbox'},status= status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenRefreshAPIView(APIView):
    pass 
# i want that asssing task function should work like this condition 
# admin