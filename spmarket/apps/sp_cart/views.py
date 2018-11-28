from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from db.base_view import BaseVerifyView
from sp_goods.models import GoodsSku
from django_redis import get_redis_connection

#添加数据
class AddCartView(View):
    def get(self, request):
        pass
    def post(self, request):
        # 1.需要验证登陆
        user_id = request.session.get("ID")
        if user_id is None:
            # 没有登录
            return JsonResponse({"code": 1, "errmsg": "没有登录!"})

        # 2. 接收参数: 购物车加入数量(count),当前商品ID(sku_id)
        sku_id = request.POST.get("sku_id")
        count = request.POST.get("count")
        # 都必须为整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            # 参数错误
            return JsonResponse({'code': 2, "errmsg": "参数错误!"})
        # # count必须大于0
        # if count <= 0:
        #     # 参数错误
        #     return JsonResponse({'code': 3, "errmsg": "参数错误!"})
        # c.商品必须存在
        try:
            goodssku = GoodsSku.objects.get(pk=sku_id)
        except GoodsSku.DoesNotExist:
            # 商品不存在
            return JsonResponse({'code': 4, "errmsg": "商品不存在!"})

        # d.(可以有)判断库存
        if goodssku.stock < count:
            # 库存不足
            return JsonResponse({'code': 5, "errmsg": "库存不足!"})

        # 添加商品到购物车中(通过redis实现)
        r = get_redis_connection('default')
        # 操作redis
        cart_key = "cart_key_{}".format(user_id)
        # 存储到redis中
        sku_id_count = r.hincrby(cart_key, sku_id, count)
        # 判断当前sku_id中的数量如果等于0说明 需要从redis中删除该sku_id对应的键
        if sku_id_count == 0:
            r.hdel(cart_key, sku_id)
        # 获取购物车中总数量
        cart_count = 0
        # 取值
        cart_values = r.hvals(cart_key)
        for v in cart_values:
            cart_count += int(v)

        # 返回成功
        return JsonResponse({"code": 0, "cart_count": cart_count})


#购物车

class ShopCartView(BaseVerifyView):
    def get(self,request):
        r = get_redis_connection("default")
        #获取redis中的数据
        cart_key ="cart_key_{}".format(request.session.get('ID'))
        cart_data = r.hgetall(cart_key)
        goodsskus = []
        for sku_id,count in cart_data.items():
            sku_id = int(sku_id)
            count = int(count)

            goodssku = GoodsSku.objects.get(pk = sku_id)

            goodssku.count = count

            goodsskus.append(goodssku)

        context = {
            "goodsskus" : goodsskus
        }

        return render(request,'sp_cart/shopcart.html', context)


    def post(self, request):
        pass
