from django.contrib import admin

from food_shop.food_app.models import CookedFood, Chef, EBook, CustomUser


# Creates a drag for the price filter
class PriceRangeFilter(admin.SimpleListFilter):
    title = 'Price Range'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('0-10', '0 - 10'),
            ('10-50', '10 - 50'),
            ('50-100', '50 - 100'),
            ('100-500', '100 - 500'),
            ('500+', '500+'),
        )

    def queryset(self, request, queryset):
        if self.value():
            min_price, max_price = self.value().split('-')
            return queryset.filter(price__gte=min_price, price__lte=max_price)


class EbookAdmin(admin.ModelAdmin):
    # Customize the list display columns
    list_display = ('title', 'chef', 'total_dishes')

    # Add filters for certain fields
    list_filter = ('total_dishes',)

    # Add search fields for searching by specific fields
    search_fields = ('title', 'chef__first_name')

    # Define ordering of records
    ordering = ('total_dishes',)

    # Customize the form used for adding/editing records
    # fields = ('title', 'chef', 'total_dishes', 'total_breakfast_dishes', 'total_lunch_dishes', 'total_dinner_dishes')

    # Customize the raw_id_fields widget for a foreign key field
    raw_id_fields = ('chef',)


class ChefAdmin(admin.ModelAdmin):
    # Customize the list display columns
    list_display = ('first_name', 'last_name', 'chef_degree', 'nationality', 'cooked_dishes')

    # Add filters for certain fields
    list_filter = ('chef_degree', 'cooked_dishes')

    # Add search fields for searching by specific fields
    search_fields = ('chef_degree', 'first_name', 'nationality')

    # Define ordering of records
    ordering = ('cooked_dishes',)


class CookedFoodAdmin(admin.ModelAdmin):
    # Customize the list display columns
    list_display = ('food_name', 'food_type', 'price',)

    # Add filters for certain fields
    list_filter = ('food_type', PriceRangeFilter)

    # Add search fields for searching by specific fields
    search_fields = ('food_name', 'food_type',)

    # Define ordering of records
    ordering = ('price',)


admin.site.register(CustomUser)
admin.site.register(CookedFood, CookedFoodAdmin)
admin.site.register(Chef, ChefAdmin)
admin.site.register(EBook, EbookAdmin)
