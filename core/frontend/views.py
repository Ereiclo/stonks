from django.shortcuts import render
from django.views import View


# -------------------------------- TEMPORARY --------------------------------


class IndexView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LoginView(View):
    template_name = "accounts/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RegisterView(View):
    template_name = "accounts/register.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AccountView(View):
    template_name = "accounts/account.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UpdateView(View):
    template_name = "accounts/update.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class PortfolioView(View):
    template_name = "stocks/portfolio.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)