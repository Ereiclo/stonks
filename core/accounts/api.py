from django.contrib.auth import login
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken as KnoxAuthToken
from knox.views import LoginView as KnoxLoginView
from .serializers import UserDetailsSerializer, RegisterSerializer, ChangePasswordSerializer


class RegisterAPI(generics.GenericAPIView):
    """
    Register User and return Token
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = KnoxAuthToken.objects.create(user)
        return Response({
            "users": UserDetailsSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1]
        })


class LoginAPI(KnoxLoginView):
    """
    Login User and return Token
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class UserDetailsAPI(generics.RetrieveUpdateAPIView):
    """
    Get or Update User Data
    """
    serializer_class = UserDetailsSerializer

    def get_object(self):
        return self.request.user



class ChangeUserDataAPI(generics.UpdateAPIView):
    """
    Change user password
    """
    serializer_class = UserDetailsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

class ChangePasswordAPI(generics.UpdateAPIView):
    """
    Change user password
    """
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

