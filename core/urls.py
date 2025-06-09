from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
