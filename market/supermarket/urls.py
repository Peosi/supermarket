from django.conf.urls import url

from supermarket.views import login, index, reg, forgetpassword, member, allorder, shopcar, message, gladdress

urlpatterns = [
    url(r'^$', index, name="index"), #首页
    url(r'^login/$', login, name="login"), #登录
    url(r'^reg/$', reg, name="reg"), #注册
    url(r'^forgetpassword/$', forgetpassword, name="forgetpassword"), #忘记密码
    url(r'^member/$', member, name="member"), #个人中心
    url(r'^allorder/$', allorder, name="allorder"), #全部订单
    url(r'^shopcar/$', shopcar, name="shopcar"), #购物车
    url(r'^message/$', message, name="message"), #动态
    url(r'^gladdress/$', gladdress, name="gladdress"), #收货地址
]