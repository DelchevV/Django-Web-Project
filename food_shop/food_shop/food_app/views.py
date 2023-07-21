from django.contrib.auth import views as auth_views, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import CustomUser, Recipe
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import RegisterUserModelForm, ProfileUpdateModelForm, RecipeModelForm, RecipeEditModel, \
    RecipeCreateModelForm
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


# Here will define all CRUD operation about Recipes and all other things about recipes

class RecipeCreateView(LoginRequiredMixin, views.CreateView):
    model = Recipe
    form_class = RecipeCreateModelForm
    template_name = 'recipes/create-recipe.html'
    success_url = reverse_lazy('dashboard')
    print("hey we are here")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)


def dashboard(request):
    recipes = Recipe.objects.all()
    context = {
        "recipes": recipes
    }
    return render(request, 'recipes/dashboard.html', context)


class RecipeEdit(LoginRequiredMixin, views.UpdateView):
    model = Recipe
    form_class = RecipeEditModel
    template_name = 'recipes/edit-recipe.html'
    success_url = reverse_lazy('dashboard')


class RecipeDelete(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    model = Recipe
    template_name = 'recipes/delete-recipe.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def handle_no_permission(self):
        if self.raise_exception:
            # If 'raise_exception' is True (default), return a 403 Forbidden response
            return HttpResponseForbidden("You do not have permission to delete this recipe.")
        else:
            # If 'raise_exception' is False, redirect to a different URL
            return HttpResponseRedirect(reverse_lazy('delete-error'))


def delete_error(request):
    return render(request, 'common/non-authorized-deletion.html')


@login_required()
def details(request, pk):
    recipe = Recipe.objects.filter(pk=pk).get()
    user = request.user
    print()
    print()
    context = {
        'recipe': recipe,
        'user': user
    }
    return render(request, 'recipes/details-recipe.html', context)
