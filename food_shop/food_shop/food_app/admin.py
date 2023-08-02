from django.contrib import admin

from food_shop.food_app.models import CookedFood, Chef, EBook

admin.site.register(CookedFood)
admin.site.register(Chef)
admin.site.register(EBook)
