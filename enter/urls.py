from django.urls import path, include
from .views import LoginEnterForm
urlpatterns = [
    path('', LoginEnterForm.as_view(), name="login_enter"),
]