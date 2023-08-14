from django.contrib.auth import views as auth_views, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
import requests
from .models import CustomUser, Recipe, EBook, CookedFood, Chef
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import RegisterUserModelForm, ProfileUpdateModelForm, RecipeEditModel, \
    RecipeCreateModelForm, FeedBackModelForm, BookModelForm, ChefModelForm
from django.views import generic as views
from django.views.generic import FormView


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


@login_required()
def profile_details(request):
    user = request.user
    recipes = Recipe.objects.all()
    books = EBook.objects.all()
    chefs = Chef.objects.all()
    context = {
        'user': user,
        'books': books,
        'recipes': recipes,
        'chefs': chefs
    }
    return render(request, 'users/profile-details.html', context)


# Here will define all CRUD operation about Recipes and all other things about recipes

class RecipeCreateView(LoginRequiredMixin, views.CreateView):
    model = Recipe
    form_class = RecipeCreateModelForm
    template_name = 'recipes/create-recipe.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)


@login_required()
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


class ProfileDelete(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    model = CustomUser
    template_name = "users/delete-user.html"
    success_url = reverse_lazy('index')

    def test_func(self):
        # Check if the user making the request is the same user to be deleted
        return self.get_object() == self.request.user


@login_required()
def dashboard_own(request):
    user_pk = request.user.pk
    recipes = Recipe.objects.filter(pk=user_pk).all()
    context = {
        "recipes": recipes
    }
    return render(request, 'recipes/dashboard.html', context)


class FeedbackView(LoginRequiredMixin, FormView):
    template_name = 'feedback_email_form.html'
    form_class = FeedBackModelForm
    success_url = reverse_lazy('profile-details')  # Replace with the URL of the success page

    def form_valid(self, form):
        # Send the email using Google's SMTP settings
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = self.request.user.email  # Replace with your Gmail email address
        recipient_list = ['veselindelchev39@gmail.com', ]

        send_mail(subject, message, from_email, recipient_list)

        # Redirect to the success page after sending the email
        return super().form_valid(form)


@login_required()
def menu(request):
    foods = CookedFood.objects.all()
    context = {
        'foods': foods
    }
    return render(request, 'menu/dashboard.html', context)


@login_required()
def chefs(request):
    chefs = Chef.objects.all()
    context = {
        'chefs': chefs
    }
    return render(request, 'chefs/dashboard.html', context)


class CreateChef(LoginRequiredMixin, views.CreateView):
    model = Chef
    template_name = 'chefs/create.html'
    form_class = ChefModelForm
    success_url = reverse_lazy('profile-details')

    def form_valid(self, form):
        return super().form_valid(form)


@login_required()
def books(request):
    books = EBook.objects.all()
    context = {
        'books': books
    }
    return render(request, 'books/dashboard.html', context)


@login_required()
def download_book(request, pk):
    try:
        # Retrieve the EBook object from the database using the given ebook_id
        ebook = EBook.objects.get(pk=pk)

        # Get the URL of the PDF file from the EBook object
        pdf_url = ebook.url

        # Send a GET request to the URL to get the PDF file
        response = requests.get(pdf_url)

        # Check if the request was successful and the content type is PDF
        if response.status_code == 200 and response.headers['content-type'] == 'application/pdf':
            # Set the appropriate content type for the response
            response = HttpResponse(response.content, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="CookBook.pdf"'
            return response
        else:
            # Handle the case when the file couldn't be downloaded
            return HttpResponse('Error: PDF file not found or cannot be downloaded.', status=404)

    except EBook.DoesNotExist:
        # Handle the case when the EBook object does not exist in the database
        return HttpResponse('Error: EBook not found.', status=404)


@login_required()
def details_book(request, pk):
    book = EBook.objects.filter(pk=pk).get()
    context = {
        'book': book
    }
    return render(request, 'books/details_book.html', context)


class CreateBook(LoginRequiredMixin, views.CreateView):
    model = EBook
    template_name = 'books/create.html'
    form_class = BookModelForm
    success_url = reverse_lazy('profile-details')

    def form_valid(self, form):
        return super().form_valid(form)
