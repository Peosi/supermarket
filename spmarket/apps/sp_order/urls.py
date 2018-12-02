from django.conf.urls import url

from sp_order.views import TrueOrderView, OrderView, success, pay

urlpatterns = [
    url(r'^trueorder/$', TrueOrderView.as_view(), name="true_order"),  # 确认订单
    url(r'^order/$', OrderView.as_view(), name="order"),  # 确认支付
    url(r'^pay/$', pay, name="发起支付"),
    url(r'^success/$', success, name="支付成功"),

]
