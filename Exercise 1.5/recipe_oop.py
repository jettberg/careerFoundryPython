# recipe_oop.py

from __future__ import annotations


class Recipe:
    # Class variable to store all ingredients across all recipes
    all_ingredients = []

    def __init__(self, name: str):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None

    # Getter & Setter for name
    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    # Getter & Setter for cooking_time
    def get_cooking_time(self) -> int:
        return self.cooking_time

    def set_cooking_time(self, cooking_time: int) -> None:
        self.cooking_time = cooking_time
        # If cooking time changes, difficulty should be recalculated
        self.difficulty = None

    # Add ingredients (variable-length arguments)
    def add_ingredients(self, *ingredients: str) -> None:
        for ing in ingredients:
            if isinstance(ing, str) and ing.strip() != "":
                self.ingredients.append(ing.strip())
        self.update_all_ingredients()
        # ingredients changed -> difficulty may change
        self.difficulty = None

    # Getter for ingredients
    def get_ingredients(self) -> list:
        return self.ingredients

    # Calculate & update difficulty
    def calculate_difficulty(self) -> None:
        num_ingredients = len(self.ingredients)

        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    # Getter for difficulty (auto-calc if needed)
    def get_difficulty(self) -> str:
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty

    # Search for ingredient in this recipe
    def search_ingredient(self, ingredient: str) -> bool:
        return ingredient in self.ingredients

    # Update class variable all_ingredients
    def update_all_ingredients(self) -> None:
        for ing in self.ingredients:
            if ing not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ing)

    # String representation
    def __str__(self) -> str:
        return (
            f"Recipe: {self.name}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Ingredients: {', '.join(self.ingredients)}\n"
            f"Difficulty: {self.get_difficulty()}"
        )


def recipe_search(data: list[Recipe], search_term: str) -> None:
    print(f"\n=== Searching for recipes with ingredient: {search_term} ===")
    found_any = False

    for recipe in data:
        if recipe.search_ingredient(search_term):
            print("\n" + str(recipe))
            found_any = True

    if not found_any:
        print("No recipes found with that ingredient.")


if __name__ == "__main__":
    # Create recipes

    tea = Recipe("Tea")
    tea.add_ingredients("Tea Leaves", "Sugar", "Water")
    tea.set_cooking_time(5)
    print(tea)

    coffee = Recipe("Coffee")
    coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
    coffee.set_cooking_time(5)
    print("\n" + str(coffee))

    cake = Recipe("Cake")
    cake.add_ingredients(
        "Sugar",
        "Butter",
        "Eggs",
        "Vanilla Essence",
        "Flour",
        "Baking Powder",
        "Milk",
    )
    cake.set_cooking_time(50)
    print("\n" + str(cake))

    banana_smoothie = Recipe("Banana Smoothie")
    banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
    banana_smoothie.set_cooking_time(5)
    print("\n" + str(banana_smoothie))

    # Wrap into recipes_list
    recipes_list = [tea, coffee, cake, banana_smoothie]

    # Search for recipes containing each ingredient
    recipe_search(recipes_list, "Water")
    recipe_search(recipes_list, "Sugar")
    recipe_search(recipes_list, "Bananas")