from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, Ingredient


class RecipeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.salt = Ingredient.objects.create(name="Salt")
        self.pepper = Ingredient.objects.create(name="Pepper")

        self.recipe = Recipe.objects.create(
            name="Test Soup",
            description="A simple test soup",
            cooking_time=5,
            created_by=self.user,
        )
        self.recipe.ingredients.add(self.salt, self.pepper)

    def test_ingredient_str(self):
        self.assertEqual(str(self.salt), "Salt")

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), "Test Soup")

    def test_difficulty_calculation_easy(self):
        # cooking_time < 10 and ingredients < 4 -> Easy
        self.assertEqual(self.recipe.calculate_difficulty(), "Easy")

    def test_difficulty_saved_on_save(self):
        # difficulty should be set after save runs
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.difficulty, "Easy")