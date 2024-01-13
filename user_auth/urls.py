from django.urls import path, include
from . import views

app_name = 'user_auth'

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
]
