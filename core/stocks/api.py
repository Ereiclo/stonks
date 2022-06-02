from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import CompanySerializer, PortafolioSerializer
from .models import Portfolio


class UserPortafolioAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = PortafolioSerializer

    def get_queryset(self):
        user = self.request.user
        return Portfolio.objects.filter(client_dni=user.dni)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PortafolioSerializer(queryset, many=True)
        return Response(serializer.data)
