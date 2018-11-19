from django.conf.urls import url

from supermarket.views import login, index, reg

urlpatterns = [
    url(r'^$', index, name="index"), #首页
    url(r'^login/$', login, name="login"), #登录
    url(r'^reg/$', reg, name="reg"), #注册
]