from django.urls import path
from .views import Register, LogOut, LogIn, index, profile_details, ProfileUpdate, RecipeCreateView, dashboard, \
    RecipeEdit, RecipeDelete, delete_error, details, ProfileDelete, dashboard_own, FeedbackView, menu, chefs, books, download_book, details_book

urlpatterns = [
    path('', index, name='index'),
    path('register/', Register.as_view(), name='register-user'),
    path('login/', LogIn.as_view(), name='login-user'),
    path('logout/', LogOut.as_view(), name='logout-user'),
    path('profile/details/', profile_details, name='profile-details'),
    path('profile/edit/<int:pk>/', ProfileUpdate.as_view(), name='profile-edit'),
    path('profile/delete/<int:pk>/', ProfileDelete.as_view(), name='profile-delete'),
    path('dashborad/', dashboard, name='dashboard'),
    path('dashboard/own/', dashboard_own, name='dashboard-own'),
    path('details/<int:pk>/', details, name='details'),
    path('recipes/create/', RecipeCreateView.as_view(), name='create-recipe'),
    path('recipe/edit/<int:pk>', RecipeEdit.as_view(), name='edit-recipe'),
    path('recipe/delete/<int:pk>', RecipeDelete.as_view(), name='delete-recipe'),
    path('recipe/delete/not-authotized', delete_error, name='delete-error'),
    path('profile/feedback/', FeedbackView.as_view(), name='feedback'),
    path('menu/', menu, name='menu'),
    path('chefs/', chefs, name='chefs'),
    path('books/', books, name='books'),
    path('books/download/<int:pk>/', download_book, name='download-book'),
    path('books/details/<int:pk>/', details_book, name='details-book')
]
