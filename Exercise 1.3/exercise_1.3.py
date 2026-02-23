# Exercise_1.3.py

# Initialize two empty lists
recipes_list = []
ingredients_list = []


def take_recipe():
    name = input("Enter recipe name: ").strip()

    while True:
        cooking_time_input = input("Enter cooking time in minutes (number): ").strip()
        try:
            cooking_time = int(cooking_time_input)
            if cooking_time < 0:
                print("Cooking time can't be negative. Try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer (e.g., 5, 12).")

    # Build ingredients list
    ingredients = []
    while True:
        num_ing_input = input("How many ingredients does this recipe have? ").strip()
        try:
            num_ingredients = int(num_ing_input)
            if num_ingredients <= 0:
                print("Enter a number greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer (e.g., 3, 5).")

    for i in range(num_ingredients):
        ing = input(f"Enter ingredient #{i+1}: ").strip()
        # Avoid blank ingredient entries
        while ing == "":
            ing = input(f"Ingredient #{i+1} can't be blank. Re-enter: ").strip()
        ingredients.append(ing)

    recipe = {"name": name, "cooking_time": cooking_time, "ingredients": ingredients}
    return recipe


def get_difficulty(recipe):
    cooking_time = recipe["cooking_time"]
    num_ingredients = len(recipe["ingredients"])

    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    else:
        return "Hard"


if __name__ == "__main__":
    # Ask user how many recipes they would like to enter
    while True:
        n_input = input("How many recipes would you like to enter? ").strip()
        try:
            n = int(n_input)
            if n <= 0:
                print("Please enter a number greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer (e.g., 1, 3, 5).")

    # Collect recipes
    for _ in range(n):
        recipe = take_recipe()

        # Update unique ingredients list
        for ingredient in recipe["ingredients"]:
            if ingredient not in ingredients_list:
                ingredients_list.append(ingredient)

        # Add recipe dictionary to recipes_list
        recipes_list.append(recipe)

    # Display recipes with difficulty
    print("\n--- Recipes List ---")
    for recipe in recipes_list:
        difficulty = get_difficulty(recipe)
        print(f"\nRecipe: {recipe['name']}")
        print(f"Cooking Time (min): {recipe['cooking_time']}")
        print(f"Ingredients: {', '.join(recipe['ingredients'])}")
        print(f"Difficulty: {difficulty}")

    # Display ingredients alphabetically
    print("\n--- Ingredients List (Alphabetical) ---")
    for ing in sorted(ingredients_list, key=str.lower):
        print(ing)