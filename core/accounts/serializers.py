from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Client


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('dni', 'names', 'lastname', 'email')

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('dni', 'names', 'lastname', 'email','password')
        extra_kwargs = {'password': {'write_only': True,'required':False},
                        'dni': {'write_only':True}}
    def update(self,instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')  
            instance.set_password(password)
        return super().update(instance,validated_data)
            



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('dni', 'names', 'lastname', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Client.objects.create_user(validated_data['dni'],
                                          validated_data['names'],
                                          validated_data['lastname'],
                                          validated_data['email'],
                                          validated_data['password'])
        return user
