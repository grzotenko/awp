from django.urls import path, include
from django.conf.urls import url

from .views import *
urlpatterns = [
    path('', MainWarehouse.as_view(), name="warehouse_main"),
    url(r'^WarehouseFilter/$', WarehouseFilter),
    url(r'^WrhsIn$', WrhsIn),
    url(r'^VolumeFilter/$', VolumeFilter),
    url(r'^AmountFilter/$', AmountFilter),
    url(r'^WrhsOut/$', WrhsOut),
    url(r'^wrhsPeriod/$', wrhsPeriod),
    url(r'^export/$',wrhsExport),
    url(r'^sendMessage/$', exportClick),
]