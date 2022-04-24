from datetime import datetime
from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from dj_rest_auth.serializers import UserDetailsSerializer
from django.core import exceptions
import django.contrib.auth.password_validation as validators

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = [field.name for field in model._meta.fields]

class UserSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = models.User
        fields = [field.name for field in model._meta.fields]
        extra_kwargs = {'password': {'write_only': True},
        'date_joined': {'read_only': True, 'required': False},}
        
    def validate(self, data):
        """
        raise validation error if anyone of first_name, last_name or email fields are empty
        """
        message_dic = {} 
        user = User(**data)
        try:
            validators.validate_password(password = data['password'], user=User)
        except exceptions.ValidationError as e:
            message_dic['password'] = list(e.messages)
        for field in ['first_name', 'last_name', 'email']:
            if data.get(field, '').strip() == '':
                message_dic[field] = "cannot be empty"
        if message_dic: 
            raise serializers.ValidationError(message_dic)
        return data

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_superuser = False
        user.is_staff = False
        user.is_active = True
        user.date_joined = datetime.now()
        user.save()
        # by default, create a customer user profile for each user
        user_profile = models.UserProfile(user=user, type='customer')
        user_profile.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['type']

class UserSerializerTwo(UserDetailsSerializer):
    """
    User model w/o password
    """
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('pk','username', 'email', 'first_name', 'last_name' ,'profile')
        read_only_fields = ('email', )
    