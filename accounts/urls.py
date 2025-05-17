from django.urls import path
from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('converter.urls'), name='home'),  # Add this line
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_request, name='login'),  # Add if missing
    path('password-change/', 
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change.html'
        ), 
        name='password_change'),
path('password-change/done/', 
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'
        ), 
        name='password_change_done'),
]