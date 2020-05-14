from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('day',)

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('cash_now',)

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)