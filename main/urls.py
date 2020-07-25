from django.urls import path, include
from .views import *
urlpatterns = [
    path('', MainSession.as_view(), name="session_main"),
    path('stop/', stopView, name="session_stop"),
    path('print/', printView, name="session_print"),
    path('pay/', payView, name="session_pay"),
    path('payfinal/<int:payment>', payFinal.as_view(), name="session_payfinal"),
    path('delete/', deleteView, name="session_delete"),
    path('new/', NewSession.as_view(), name="session_new"),
    path('edit/<int:id>', EditSession.as_view(), name='session_edit'),
    path('tariff/<int:id>/', tariffChange, name="session_form_change_tariff"),
    path('discount/<int:id>/', discountChange, name="session_form_change_discount"),
]