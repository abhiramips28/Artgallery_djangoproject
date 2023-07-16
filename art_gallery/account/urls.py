from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import SignUpView

urlpatterns = [
    path('signup/',SignUpView.as_view(),name='signup'),
    re_path(r'^login/$',auth_views.LoginView.as_view(),name='login'),

]