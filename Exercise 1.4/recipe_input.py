# recipe_input.py
import pickle


def calc_difficulty(cooking_time: int, ingredients: list) -> str:
    num_ingredients = len(ingredients)

    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    else:
        return "Hard"


def take_recipe() -> dict:
    name = input("Recipe name: ").strip()

    # cooking_time (int)
    while True:
        ct = input("Cooking time in minutes: ").strip()
        try:
            cooking_time = int(ct)
            if cooking_time < 0:
                print("Cooking time can't be negative. Try again.")
                continue
            break
        except ValueError:
            print("Please enter a whole number (e.g., 5, 12).")

    # ingredients list
    ingredients = []
    while True:
        n_ing = input("How many ingredients? ").strip()
        try:
            n_ing = int(n_ing)
            if n_ing <= 0:
                print("Enter a number greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a whole number (e.g., 3).")

    for i in range(n_ing):
        ing = input(f"Ingredient #{i+1}: ").strip()
        while ing == "":
            ing = input(f"Ingredient #{i+1} can't be blank. Re-enter: ").strip()
        ingredients.append(ing)

    difficulty = calc_difficulty(cooking_time, ingredients)

    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty,
    }
    return recipe


if __name__ == "__main__":
    filename = input("Enter filename to load/save (example: recipes.bin): ").strip()

    # try-except-else-finally to load existing data or create fresh data
    try:
        file = open(filename, "rb")
        data = pickle.load(file)  # expects dict with keys: recipes_list, all_ingredients
    except FileNotFoundError:
        data = {"recipes_list": [], "all_ingredients": []}
    except Exception:
        data = {"recipes_list": [], "all_ingredients": []}
    else:
        file.close()
    finally:
        recipes_list = data.get("recipes_list", [])
        all_ingredients = data.get("all_ingredients", [])

    # Ask how many recipes
    while True:
        n = input("How many recipes would you like to enter? ").strip()
        try:
            n = int(n)
            if n <= 0:
                print("Enter a number greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a whole number (e.g., 2).")

    # Collect recipes
    for _ in range(n):
        recipe = take_recipe()
        recipes_list.append(recipe)

        for ingredient in recipe["ingredients"]:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    # Write updated data back to file
    data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

    with open(filename, "wb") as file:
        pickle.dump(data, file)

    print(f"\nSaved {len(recipes_list)} recipe(s) to '{filename}'.")