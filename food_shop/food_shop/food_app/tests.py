
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from .forms import RecipeCreateModelForm
from .models import Recipe
from .views import RecipeDelete

CustomUser = get_user_model()


class ProfileDeleteViewTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
            age=23,
        )
        self.login_successful = self.client.login(username='testuser', password='testpassword')
        self.url = reverse('profile-delete', args=[self.user.pk])

    def test_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete-user.html')

    def test_user_deletion(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
        self.assertFalse(CustomUser.objects.filter(pk=self.user.pk).exists())

    def test_unauthenticated_user_redirect(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login-user')}?next={self.url}")

    def test_access_other_users_profile(self):
        other_user = CustomUser.objects.create_user(
            username='otheruser',
            password='otherpassword',
            age=22
        )
        url = reverse('profile-delete', args=[other_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_view_requires_login(self):
        self.assertTrue(self.login_successful)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Or any other expected behavior


class ProfileDetailsViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', age=25)

        self.client.login(username='testuser', password='testpassword')

    def test_profile_details_view(self):
        response = self.client.get(reverse('profile-details'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile-details.html')
        self.assertEqual(response.context['user'], self.user)


class RecipeDetailsViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword', age=23)
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test description',
            ingredients='Ingredient 1, Ingredient 2',
            instructions='Step 1, Step 2',
            prep_time=30,
            cook_time=45,
            serving_way='hot',
            author=self.user
        )

    def test_details_view_with_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('details', args=[self.recipe.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recipe.title)
        self.assertContains(response, self.recipe.description)

    def test_details_view_context(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('details', args=[self.recipe.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['recipe'], self.recipe)
        self.assertEqual(response.context['user'], self.user)


class RecipeDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser', password='testpassword', age=24)
        cls.another_user = get_user_model().objects.create_user(username='otheruser', password='otherpassword', age=24)
        cls.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test Description',
            ingredients='Test Ingredients',
            instructions='Test Instructions',
            prep_time=10,
            cook_time=20,
            serving_way='hot',
            author=cls.user
        )

    def setUp(self):
        def setUp(self):
            self.middleware = MessageMiddleware(get_response=None)
            self.session_middleware = SessionMiddleware(get_response=None)
            self.middleware.process_request(self.client.request)
            self.session_middleware.process_request(self.client.request)

    def test_user_can_delete_own_recipe(self):
        self.client.login(username='testuser', password='testpassword', age=24)
        response = self.client.get(reverse('delete-recipe', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure you want to delete')

    def test_user_cannot_delete_other_user_recipe(self):
        self.client.login(username='otheruser', password='otherpassword', age=24)
        response = self.client.get(reverse('delete-recipe', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 302)

    def test_post_request_deletes_recipe(self):
        self.client.login(username='testuser', password='testpassword', age=24)
        response = self.client.post(reverse('delete-recipe', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_handle_no_permission_redirects(self):
        view_instance = RecipeDelete()
        view_instance.request = self.client.get(reverse('delete-recipe', args=[self.recipe.pk]))
        view_instance.object = self.recipe
        view_instance.request.user = self.another_user
        view_instance.raise_exception = False
        response = view_instance.handle_no_permission()
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse('delete-error'))


class RecipeCreateViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', age=25)
        self.client.login(username='testuser', password='testpassword')

    def test_recipe_create_view(self):
        response = self.client.get(reverse('create-recipe'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/create-recipe.html')
        self.assertIsInstance(response.context['form'], RecipeCreateModelForm)

    def test_recipe_create_view_post(self):
        form_data = {
            'title': 'Test Recipe',
            'description': 'This is a test recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'instructions': 'Step 1, Step 2',
            'prep_time': 30,
            'cook_time': 45,
            'serving_way': 'hot',  # Adjust based on your CHOICES
        }

        response = self.client.post(reverse('create-recipe'), data=form_data)

        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Recipe.objects.filter(title='Test Recipe').exists())

    def test_recipe_create_view_invalid_form(self):
        form_data = {
            # ... Missing required fields or invalid data ...
        }

        response = self.client.post(reverse('create-recipe'), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/create-recipe.html')
        self.assertContains(response, 'This field is required')

# Create your tests here.


# Integration tests
