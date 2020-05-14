from django.contrib import admin
from django import forms
from .models import *
import random
from daycalendar.models import Day
@admin.register(UserSalary)
class UserSalaryAdmin(admin.ModelAdmin):
    list_display = ('user','record_type','start','end','base','bonus','amount', 'payedProcent')

@admin.register(Weekend)
class WeekendAdmin(admin.ModelAdmin):
    list_display = ('name','date',)

@admin.register(MoneyOperations)
class MoneyOperationsAdmin(admin.ModelAdmin):
    list_display = ('name','type',)

class VacantedShiftsAdmin(admin.ModelAdmin):
    model = VacantedShifts
    list_filter = ["profile", "day", "type"]
    list_display = ["profile", "day", "type"]
admin.site.register(VacantedShifts, VacantedShiftsAdmin)

@admin.register(TypeOfMO)
class TypeOfMOAdmin(admin.ModelAdmin):
    list_display = ('name','moneyoper',)

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('name','date',)

from management.models import TYPEOfPref
def randomPrefs(modeladmin, request, queryset):
    for pref in queryset:
        r = random.randint(0,2)
        if r == 0:
            pref.pref = "="
        elif r == 1:
            pref.pref = "-"
        else:
            pref.pref = "+"
        pref.save()
randomPrefs.short_description = "Случайные предпочтения"
class PrefsAdmin(admin.ModelAdmin):
    model = Preferences
    actions = [randomPrefs]
    list_filter = ["profile","pref", "day", "type"]
    list_display = ["profile", "pref", "day", "type"]
admin.site.register(Preferences, PrefsAdmin)

def eveningActivityOnOff(modeladmin, request, queryset):
    for elem in queryset:
        elem.eveningActivity = not elem.eveningActivity
        elem.save()
eveningActivityOnOff.short_description = "Активность Резерной Смены On/Off"
def createPlan(modeladmin, request, queryset):
    CurrentPlan.objects.all().delete()
    for day in Day.objects.all():
        morning = CurrentPlan.objects.create(day=day, type="M", profile = random.choice(Profile.objects.all()))
        evening = CurrentPlan.objects.create(day=day, type="E", profile = random.choice(Profile.objects.all()))
        reserving = CurrentPlan.objects.create(day=day, type="R", profile = random.choice(Profile.objects.all()))
createPlan.short_description = "Пересоздать План"
class CurrentPlanAdmin(admin.ModelAdmin):
    model = CurrentPlan
    actions = [eveningActivityOnOff, createPlan]
    list_filter = ["profile", "day", "type"]
    list_display = ["profile", "day", "type", "eveningActivity"]
admin.site.register(CurrentPlan, CurrentPlanAdmin)
def createPlanF(modeladmin, request, queryset):
    FuturePlan.objects.all().delete()
    for day in Day.objects.all():
        morning = FuturePlan.objects.create(day=day, type="M")
        evening = FuturePlan.objects.create(day=day, type="E")
        reserving = FuturePlan.objects.create(day=day, type="R")
createPlanF.short_description = "Пересоздать План"
def editProfiles(modeladmin, request, queryset):
    for elem in queryset:
        if elem.profile is None:
            elem.profile = random.choice(Profile.objects.all())
        else:
            elem.profile = None
        elem.save()
editProfiles.short_description = "Добавить(Удалить) админов на смены"
class FuturePlanAdmin(admin.ModelAdmin):
    model = FuturePlan
    actions = [createPlanF, editProfiles]
    list_filter = ["profile", "day", "type"]
    list_display = ["profile", "day", "type"]
admin.site.register(FuturePlan, FuturePlanAdmin)