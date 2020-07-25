from django.contrib import admin
from django import forms
from .models import *

# Register your models here.
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('SID','is_active',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('CID',)

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name',)



@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(CardPay)
class CardPayAdmin(admin.ModelAdmin):
    pass

@admin.register(CashPay)
class CashPayAdmin(admin.ModelAdmin):
    pass

@admin.register(IncludeService)
class IncludeServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(AddService)
class AddServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(UseService)
class UseServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name','colortile','colorfont',)
    formfield_overrides = {
        ColorField: {'widget': forms.TextInput(attrs={'type': 'color',
                                                      'style': 'height: 100px; width: 100px;'})}
    }

