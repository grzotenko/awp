from django.contrib import admin
from django import forms
from .models import *

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name','room', 'date',)