from xml.dom import ValidationErr
from rest_framework import serializers
from company.utils import Utils

from company.utils import Utils
from .models import CustomUser,Project
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


#create serializers here      
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project  # Use your Project model or whatever model you're serializing
        fields = '__all__'
class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    id=serializers.ReadOnlyField()    
    # this meta is used to coustamize which fields do we need from the models
    # It will automatically generate a set of fields for you, based on the model. 
    # It will automatically generate validators for the serializer, such as unique_together validators.
    class Meta:
        model=CustomUser
        fields="__all__"
            # 



class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    confirmPass = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"
    def create(self, validated_data):
        confirmPass = validated_data.pop('confirmPass', None)
        if 'password' in validated_data and confirmPass:
            if validated_data['password'] != confirmPass:
                raise serializers.ValidationError("Passwords do not match")
        
        user = CustomUser.objects.create_user(**validated_data)
        return user


    def create(self, validated_data):
        return super().create(validated_data)

        
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model=CustomUser
        fields=("email","password")


class ChangePasswordSerializer(serializers.HyperlinkedModelSerializer):
    id=serializers.ReadOnlyField
    class Meta:
        model=CustomUser
        fields=["passwords",'confirmPass']

    def validate(self,attrs):
        password = attrs.get('passwords')
        confirmPass = attrs.get('confirmPass')
        user = self.context.get['user']
        if password!= confirmPass:
            raise serializers.ValidationError({"confirmPass": "Passwords do not match."})
        user.set_password(password)
        user.save()
        return attrs

class ResetPasswordEmailRequestSerializer(serializers.ModelSerializer):

    confirmPass = serializers.CharField(write_only=True)
    class Meta:
        fields  = ["email"]

    def validate_email(self, attrs):
       email = attrs.get('email')
       if CustomUser.objects.filter(email=email).exists():
            
            user =  CustomUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('user','user')
            print('Encoded UID',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('token','token')
            link = 'https://localhost:3000/api/user/reset/'+uid+'/'+token
            print('password',link)        #    this is to send Data
            body = 'Click the following link to Reset the password'+link
            data = {
                'subject':'Reset YOUR Password',
                'body': body,
                'to_email':user.email,
            }
            Utils.send_mail(data)
            return attrs
       else:
            raise ValidationErr('You are not registered User')
