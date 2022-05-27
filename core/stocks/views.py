from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic,View


# Create your views here.
def index(request):
    return HttpResponse("Demo: Stonks - Stocks App")

class IndexView(View):
    template_name = "stocks/index.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)


class RegisterView(View):
    template_name = "stocks/register.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
