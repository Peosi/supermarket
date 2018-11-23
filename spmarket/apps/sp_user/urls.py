from django.conf.urls import url

from sp_user.views import LoginView, RegView, ForgetPassView, MemeberView, InfoView, send_msg_phone, AddressView, \
    AllorderView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),  # 登陆
    url(r'^register/$', RegView.as_view(), name="register"),  # 注册
    url(r'^forget/$', ForgetPassView.as_view(), name="forget"),  # 忘记密码
    url(r'^member/$', MemeberView.as_view(), name="member"),  # 个人中心
    url(r'^info/$', InfoView.as_view(), name="info"),  # 个人资料
    url(r'^sendMsg/$', send_msg_phone, name="sendMsg"),  # 短信地址
    url(r'^gladdress/$', AddressView.as_view(), name="gladdress"),  # 收货地址
    url(r'^allorder/$', AllorderView.as_view(), name="allorder"),  # 全部订单
]