from django import forms

from .models import CustomUser, Recipe, Feedback, EBook, Chef


class RegisterUserModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'age']


class ProfileUpdateModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['age', 'birth_date', 'bio', 'profile_picture', 'first_name', 'last_name', ]


class RecipeModelForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeCreateModelForm(RecipeModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ['author']

    def __init__(self, *args, **kwargs):
        self._current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        recipe = super().save(commit=False)

        if not recipe.author:
            recipe.author = self._current_user

        if commit:
            recipe.save()
        return recipe


class RecipeEditModel(RecipeModelForm):
    pass


class FeedBackModelForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
        exclude = ['user']


class BookModelForm(forms.ModelForm):
    class Meta:
        model = EBook
        fields = '__all__'


class ChefModelForm(forms.ModelForm):
    class Meta:
        model = Chef
        fields = '__all__'
