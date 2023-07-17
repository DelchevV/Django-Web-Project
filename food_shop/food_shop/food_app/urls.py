from django.urls import path
from .views import Register, LogOut, LogIn, index

urlpatterns = [
    path('', index, name='index'),
    path('register/', Register.as_view(), name='register-user'),
    path('login/', LogIn.as_view(), name='login-user'),
    path('logout/', LogOut.as_view(), name='logout-user'),

]
