# recipe_search.py
import pickle


def display_recipe(recipe: dict) -> None:
    print("\n--------------------")
    print(f"Recipe: {recipe.get('name')}")
    print(f"Cooking Time (min): {recipe.get('cooking_time')}")
    print("Ingredients:")
    for ing in recipe.get("ingredients", []):
        print(f"- {ing}")
    print(f"Difficulty: {recipe.get('difficulty')}")
    print("--------------------")


def search_ingredient(data: dict) -> None:
    all_ingredients = data.get("all_ingredients", [])
    recipes_list = data.get("recipes_list", [])

    if not all_ingredients:
        print("No ingredients found in data.")
        return

    print("\nAvailable ingredients:")
    for i, ing in enumerate(all_ingredients):
        print(f"{i}: {ing}")

    try:
        choice = int(input("\nEnter the number of the ingredient to search: ").strip())
        ingredient_searched = all_ingredients[choice]
    except (ValueError, IndexError):
        print("Invalid selection. Please enter a valid number from the list.")
        return
    else:
        found_any = False
        print(f"\nSearching for recipes containing: {ingredient_searched}")

        for recipe in recipes_list:
            if ingredient_searched in recipe.get("ingredients", []):
                display_recipe(recipe)
                found_any = True

        if not found_any:
            print("No recipes found containing that ingredient.")


if __name__ == "__main__":
    filename = input("Enter filename to load (example: recipes.bin): ").strip()

    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)
    except FileNotFoundError:
        print("File not found. Run recipe_input.py first to create the file.")
    except Exception:
        print("Something went wrong while reading the file.")
    else:
        search_ingredient(data)