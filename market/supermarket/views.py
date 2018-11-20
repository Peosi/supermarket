from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

from supermarket.forms import RegForm, LoginForm
from supermarket.models import Users


# 登录界面

# def login(request):
#     if request.method == "POST":
#         #完成登录验证
#         mobile = request.POST.get("mobile")
#         password = request.POST.get("password")
#         try:
#             user = Users.objects.get(mobile = mobile)
#         except Users.MultipleObjectsReturned:
#             #获取多个记录
#             return redirect("supermarket:login")
#         except Users.DoesNotExist:
#             return redirect("supermarket:login")
#         #判断密码是否正确
#         if password != user.password:
#             return redirect("supermarket:login")
#         #登陆成功
#         else:
#             return redirect("supermarket:index")
#     else:
#         return render(request, '用户/login.html')
# 登录
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            mobile = data.get('mobile')
            password = data.get('password')
            try:
                user = Users.objects.get(mobile=mobile)
            except Users.MultipleObjectsReturned:
                return redirect("supermarket:login")
            except Users.DoesNotExist:
                return redirect("supermarket:login")
            if password == user.password:
                request.session['ID'] = user.pk
                return redirect("supermarket:index")
            else:
                form.errors['password'] = ['密码错误!']

        else:
            context = {
                "errors": form.errors
            }
            return render(request, "用户/login.html", context)
    return render(request, "用户/login.html")


# 注册界面
def reg(request):
    # 接收数据
    if request.method == 'POST':
        data = request.POST
        # 创建form对象
        form = RegForm(data)
        if form.is_valid():
            data = form.cleaned_data
            # 保存到数据库
            mobile = data.get('mobile')
            password = data.get('password')
            # 处理数据
            Users.objects.create(mobile=mobile, password=password)
            return redirect("supermarket:login")
        else:
            context = {
                "errors": form.errors
            }
            return render(request, "用户/reg.html", context)
    else:
        return render(request, '用户/reg.html')


# 修改密码
def forgetpassword(request):
    return render(request, '用户/forgetpassword.html')


# 首页
def index(request):
    return render(request, 'index.html')


# 个人中心

def member(request):
    return render(request, '用户/member.html')


#全部订单
def allorder(request):
    return render(request, 'allorder.html')

#购物车

def shopcar(request):
    return render(request, 'shopcar.html')


#动态
def message(request):
    return render(request, 'message.html')

#收货地址
def gladdress(request):
    return render(request,'用户/gladdress.html')
