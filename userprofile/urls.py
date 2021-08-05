from django.urls import path
from . import views
from userprofile.views import UserProfileView
from userprofile.views import UserDetailsView
from  userprofile.views import EditProfileView
from userprofile.views import LogoutView

urlpatterns = [
    path('',UserProfileView.as_view(),name='userprofile'),
    path('userprofile/',UserDetailsView.as_view(),name='userdetails'),
    path('edit_profile/',EditProfileView.as_view(), name='edit_profile'),
    path('passwordchange/',views.passwordchange, name='passwordchange'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('search',views.searchbar,name='search'),
]