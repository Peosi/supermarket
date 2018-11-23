from django.shortcuts import render

# Create your views here.
from django.views import View


class IndexView(View):
    def get(self, request):
        return render(request, 'sp_goods/index.html')
    def post(self, request):
        pass
