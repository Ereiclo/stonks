from django.shortcuts import render
from django.views import View

class PortfolioView(View):
    template_name = "stocks/portfolio.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
