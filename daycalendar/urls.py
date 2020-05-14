from django.urls import path, include
from .views import *
urlpatterns = [
    path('', MainCalendar.as_view(), name="calendar_main"),
]