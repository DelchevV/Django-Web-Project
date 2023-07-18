from django.urls import path
from .views import Register, LogOut, LogIn, index, profile_details, ProfileUpdate

urlpatterns = [
    path('', index, name='index'),
    path('register/', Register.as_view(), name='register-user'),
    path('login/', LogIn.as_view(), name='login-user'),
    path('logout/', LogOut.as_view(), name='logout-user'),
    path('profile/details/', profile_details, name='profile-details'),
    path('profile/edit/<int:pk>', ProfileUpdate.as_view(), name='profile-edit')
]
