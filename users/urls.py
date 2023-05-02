from django.urls import path
from users.views import Registeration

urlpatterns = [
    path('register/', Registeration.as_view(), name='register'),
]
