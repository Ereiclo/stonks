from django.shortcuts import render
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Create your views here.
"""
def index(request):
    return HttpResponse("Demo: Stonks - Stocks App")
"""

class IndexView(APIView):
    template_name = "stocks/index.html"
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)

class LoginView(View):
    template_name = "stocks/login.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)


class RegisterView(View):
    template_name = "stocks/register.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)


class AccountView(View):
    template_name = "stocks/account.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)

class UpdateView(View):
    template_name = "stocks/update.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)



