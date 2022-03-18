from django.contrib import admin
from recipes.models import Ingredient, Recipe


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


class IngredientAdmin(admin.ModelAdmin):
    readonly_fields = ["sku"]


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ["sku"]
    inlines = [RecipeIngredientInline]


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
