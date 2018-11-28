# Create your views here.
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect

from sp_goods.models import GoodsSku, Cycle, Activity, Special, GoodsClass
from django_redis import get_redis_connection

# 首页
def index(request):
    # 轮播图
    cycles = Cycle.objects.filter(isDelete=False).order_by("-order")
    # 活动专区
    acts = Activity.objects.filter(isDelete=False)
    # 首页活动专区
    spe = Special.objects.filter(is_on_sale=True, isDelete=False).order_by("-order")
    context = {
        "cycles": cycles,
        "acts": acts,
        "spe": spe
    }
    return render(request, 'sp_goods/index.html', context)


# 分类页
def category(request, cate_id, order):
    # 类型转换
    try:
        cate_id = int(cate_id)
        order = int(order)
    except:
        return redirect("sp_goods:首页")
    # 导航栏
    goodclasses = GoodsClass.objects.filter(isDelete=False)

    #查询某个分类下的商品
    if cate_id == 0:
        goodclass = goodclasses.first()
        cate_id = goodclass.pk
    # 所有商品
    goodsSkus = GoodsSku.objects.filter(is_on_sale=True, isDelete=False, category_id = cate_id)
    #排序
    order_rule = ["id", "-sales", "-price", "price", "-add_time"]
    try:
        order_one = order_rule[order]
    except:
        order_one = order_rule[0]
        order = 0
    goodsSkus = goodsSkus.order_by(order_one)

    # 对数据进行分页
    pageSize = 10
    paginator = Paginator(goodsSkus, pageSize)

    # 获取某页数据
    p = request.GET.get('p', 1)
    try:
        page = paginator.page(p)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page = paginator.page(1)

    #显示购物车商品
    cart_count = 0
    if request.session.get("ID"):
        user_id = request.session.get("ID")
        # 登陆, 从redis中取出购物车中的数据
        r = get_redis_connection("default")
        # 准备键
        cart_key = "cart_key_{}".format(user_id)
        # 取值
        cart_values = r.hvals(cart_key)
        for v in cart_values:
            cart_count += int(v)



    context = {
        "goodclasses": goodclasses,
        "goodsSkus": page,
        "cate_id": cate_id,
        "order":order,
        "cart_count":cart_count,

    }
    return render(request, "sp_goods/category.html", context)


# 详情页

def detail(request, id):
    try:
        goodsSku = GoodsSku.objects.get(pk=id, is_on_sale=True)
    except GoodsSku.DoesNotExist:
        # 跳转到首页
        return redirect("sp_goods:首页")

        # 渲染数据到页面
    context = {
        "goodsSku": goodsSku
    }
    return render(request, 'sp_goods/detail.html', context)
