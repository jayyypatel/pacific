from django.urls import path
from . import views
from django.contrib.auth import views as auth_views #import this

app_name = 'auth_system'


urlpatterns = [
    path('login_user/',views.login_user,name='login_user'),
    path('register_user/',views.register_user,name='register_user'),
    path('logout_user/',views.logout_user,name='logout_user'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth_system/password_reset_done.html'), name='password_reset_done'),#second
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="auth_system/password_reset_confirm.html",success_url="/auth_system/login_user/"), name='password_reset_confirm'),#third
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth_system/password_reset_complete.html'), name='password_reset_complete'), #four

    path("password_reset", views.password_reset_request, name="password_reset")#first
]
