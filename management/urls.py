from django.urls import path, include
from .views import *
urlpatterns = [
    path('', MainManagement.as_view(), name="management_main"),
    path('addreserved/<str:adminname>', addReserved.as_view(), name="management_addreserved"),
    path('transfer/<str:adminname>', transferAdmin.as_view(), name="management_transfer"),
    path('exit', exitMenu.as_view(), name="management_exit"),
    path('exit/all/', exitAll, name="management_exit_all"),
    path('exit/report/', reportAll.as_view(), name="management_exit_report"),
    path('removereserved/', removeReserved, name="management_removereserved"),
    path('givevacant/', giveVacant, name="management_givevacant"),
    path('takevacant/', takeVacant, name="management_takevacant"),
    path('saveprefs/', savePrefs, name="management_saveprefs"),
]