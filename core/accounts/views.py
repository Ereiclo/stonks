from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions


class IndexView(View):
    template_name = "stocks/index.html"

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



