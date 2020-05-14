from django.contrib import admin
from .fields import ColorField
from django import forms
from .models import *
from daycalendar.models import Day
from management.models import Preferences
# Register your models here.
def new_profile(modeladmin, request, queryset):
    for user in queryset:
        for d in Day.objects.all():
            p1 = Preferences.objects.create(day=d, type="M", profile = user)
            p2 = Preferences.objects.create(day=d, type="E", profile = user)
new_profile.short_description = "Добавить новому админу предпочтения"
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    actions = [new_profile]
    list_display = ('user','colortile',)
    formfield_overrides = {
            ColorField: {'widget': forms.TextInput(attrs={'type': 'color',
                'style': 'height: 100px; width: 100px;'})}
        }