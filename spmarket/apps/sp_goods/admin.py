from django.contrib import admin

# Register your models here.
from sp_goods.models import GoodsClass, GoodsSpu, GoodsSku, GoodsImg, Cycle, Activity, Special, SpecialGoods

admin.site.register(GoodsClass)
admin.site.register(GoodsSpu)
admin.site.register(GoodsSku)
admin.site.register(GoodsImg)
admin.site.register(Cycle)
admin.site.register(Activity)
admin.site.register(Special)
admin.site.register(SpecialGoods)