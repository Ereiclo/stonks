from django.contrib.auth import login
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken as KnoxAuthToken
from knox.views import LoginView as KnoxLoginView
from .serializers import UserSerializer, RegisterSerializer,UpdateSerializer


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
            "users": UserSerializer(user, context=self.get_serializer_context()).data,
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
    Get and Update User
    """
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UpdateUserAPI(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = UpdateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user,data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'new name': user.names})

