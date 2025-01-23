from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('login/', views.loginPage, name='LoginPage'),
    path('signup/', views.signupPage, name='SignupPage'),
    path('forgotPwd/', views.forgotPwdPage, name='ForgotPasswordPage'),
    path('changePwd/', views.changePwdPage, name='ChangePasswordPage'),
    path('dashboard/', views.dashboardPage, name='DashboardPage'),
    path('profile/', views.profilePage, name='ProfilePage'),
    path('logout/', views.logoutPage, name='LogoutPage'),
]
