# serializers.py
from rest_framework import serializers
from .models import User, Organization

from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone_number', 'blood_group', 'district', 'province', 'user_type', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            blood_group=validated_data['blood_group'],
            district=validated_data['district'],
            province=validated_data['province'],
            user_type=validated_data.get('user_type', 'user')  # Default to 'user'
        )
        return user



from django.contrib.auth.hashers import make_password

class OrganizationRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'email', 'password', 'available_no_of_pints_of_blood', 'district', 'province']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        organization = Organization.objects.create(**validated_data)
        return organization


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = ['name' , 'email' , 'phone_number' , 'blood_group' , 'province' , 'district' , 'password']
        extra_kwargs = {
            'email': {'read_only': True},
            'blood_group': {'read_only':True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password' , None)
        if password:
            instance.password = make_password(password)

        for attr , value in validated_data.items():
            setattr(instance,attr,value)

        instance.save()
        return instance


class OrganizationProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = Organization
        fields = ['name' , 'email'  , 'province' , 'district' , 'password']
        extra_kwargs = {
            'email': {'read_only': True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password' , None)
        if password:
            instance.password = make_password(password)

        for attr , value in validated_data.items():
            setattr(instance,attr,value)

        instance.save()
        return instance
