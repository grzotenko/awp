from django.urls import path, include
from .views import *
urlpatterns = [
    path('', MainBooking.as_view(), name="booking_main"),
    path('edit/<int:id>', EditBooking.as_view(), name='booking_edit'),
    path('new', NewBooking.as_view(), name='booking_new'),
]