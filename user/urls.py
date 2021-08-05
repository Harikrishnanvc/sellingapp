from django.urls import path
from . import views
from user.views import RegisterView
from user.views import ForgotPasswordView
from user.views import LoginPageView
from user.views import EmailAuthenticationView
from user.views import PasswordChangeView


urlpatterns = [
    path('welcome/', views.WelcomeView.as_view(),name='WelcomeView'),
    path('register/', RegisterView.as_view(), name='register'),
    path('loginn/', LoginPageView.as_view(),name='login'),
    path('forgotpassword/',ForgotPasswordView.as_view(),name='forgotpassword'),
    path('emailauthentication/',EmailAuthenticationView.as_view(),name='emailauthentication'),
    path('changepassword/',PasswordChangeView.as_view(),name='changepassword'),
    path('account-verify/<slug:Token>',views.account_verify,name='account-verify'),


]