from django.contrib import admin
from .models import Recipe, Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["name", "cooking_time", "difficulty", "created_by", "created_at"]
    list_filter = ["difficulty", "created_by"]
    search_fields = ["name", "ingredients__name"]