from django.contrib.auth import views as auth_views, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import CustomUser

from .forms import RegisterUserModelForm, ProfileUpdateModelForm
from django.views import generic as views


class Register(views.CreateView):
    template_name = 'users/register.html'
    form_class = RegisterUserModelForm
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        user = form.save(commit=False)
        # Set the password using the set_password() method to ensure proper encryption
        user.set_password(form.cleaned_data['password'])
        # Save the user to the database
        user.save()

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        login(self.request, user)

        return super().form_valid(form)


class LogIn(auth_views.LoginView):

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    template_name = 'users/login.html'


class LogOut(auth_views.LogoutView):
    pass


class ProfileUpdate(views.UpdateView):
    model = CustomUser
    form_class = ProfileUpdateModelForm
    template_name = 'users/edit-user.html'
    success_url = reverse_lazy('profile-details')


def index(request):
    users = CustomUser.objects.all()
    context = {
        "users": users
    }
    return render(request, 'common/index.html', context)


@login_required
def profile_details(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'users/profile-details.html', context)
