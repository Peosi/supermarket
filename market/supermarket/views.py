
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
#登录界面
from supermarket.models import Users


def login(request):
    if request.method == "POST":
        #完成登录验证
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        try:
            user = Users.objects.get(mobile = mobile)
        except Users.MultipleObjectsReturned:
            #获取多个记录
            return redirect("supermarket:login")
        except Users.DoesNotExist:
            return redirect("supermarket:login")
        #判断密码是否正确
        if password != user.password:
            return redirect("supermarket:login")
        #登陆成功
        else:
            return redirect("supermarket:index")
    else:
        return render(request,'login.html')
#注册界面
def reg(request):
    #接收数据
    if request.method == 'POST':
        data = request.POST
        mobile = data.get('mobile')
        password = data.get('password')
        #处理数据
        Users.objects.create(mobile=mobile,password = password)
        return redirect("supermarket:login")
    else:
        return render(request, 'reg.html')
#首页
def index(request):
    return render(request,'login.html')
