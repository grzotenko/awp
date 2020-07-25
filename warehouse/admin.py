from django.contrib import admin
from .models import *
class adminCat(admin.ModelAdmin):
    model = Categories
    def save_model(self, request, obj, form, change):
        obj.cat_title = obj.cat_title.replace(' ', '_')
        obj.save()

class adminSub(admin.ModelAdmin):
    model = Subcategories
    def save_model(self, request, obj, form, change):
        obj.subcat_title = obj.subcat_title.replace(' ', '_')
        obj.save()

class adminGood(admin.ModelAdmin):
    model = Goods
    def save_model(self, request, obj, form, change):
        obj.title = obj.title.replace(' ', '_')
        obj.save()

admin.site.register(Categories, adminCat)
admin.site.register(Subcategories, adminSub)
admin.site.register(Goods, adminGood)
admin.site.register(WarehouseInOut)
# admin.site.register(Volumes)
# admin.site.register(Costs)
#admin.site.register(WhatsApp)
