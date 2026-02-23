import mysql.connector


def calculate_difficulty(cooking_time, ingredients):
    """Return difficulty string based on cooking_time and number of ingredients."""
    num_ingredients = len(ingredients)

    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    else:
        return "Hard"


def create_recipe(conn, cursor):
    print("\n--- Create a New Recipe ---")
    name = input("Recipe name: ").strip()

    while True:
        try:
            cooking_time = int(input("Cooking time (minutes): ").strip())
            if cooking_time < 0:
                print("Cooking time can't be negative. Try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for cooking time.")

    ingredients = []
    print("Enter ingredients one at a time. Type 'done' when finished.")
    while True:
        item = input("Ingredient: ").strip()
        if item.lower() == "done":
            break
        if item:
            ingredients.append(item)

    difficulty = calculate_difficulty(cooking_time, ingredients)
    ingredients_str = ", ".join(ingredients)

    sql = """
        INSERT INTO Recipes (name, ingredients, cooking_time, difficulty)
        VALUES (%s, %s, %s, %s)
    """
    val = (name, ingredients_str, cooking_time, difficulty)
    cursor.execute(sql, val)
    conn.commit()

    print("\n✅ Recipe added successfully!")


def search_recipe(conn, cursor):
    print("\n--- Search Recipes by Ingredient ---")

    # Get all ingredients strings
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    # Build unique ingredients list
    all_ingredients = []
    for row in results:
        # row is like ('Milk, Sugar, Eggs',)
        ing_str = row[0] or ""
        parts = [p.strip() for p in ing_str.split(",") if p.strip()]
        for p in parts:
            if p not in all_ingredients:
                all_ingredients.append(p)

    if not all_ingredients:
        print("No ingredients found. Add recipes first.")
        return

    # Display numbered list
    print("\nAvailable ingredients:")
    for idx, ing in enumerate(all_ingredients, start=1):
        print(f"{idx}. {ing}")

    try:
        choice = int(input("\nPick an ingredient number to search: ").strip())
        if choice < 1 or choice > len(all_ingredients):
            print("Invalid number choice.")
            return
        search_ingredient = all_ingredients[choice - 1]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # Search with LIKE + wildcard
    query = """
        SELECT id, name, ingredients, cooking_time, difficulty
        FROM Recipes
        WHERE ingredients LIKE %s
    """
    cursor.execute(query, (f"%{search_ingredient}%",))
    matches = cursor.fetchall()

    print(f"\nResults for ingredient: {search_ingredient}")
    if not matches:
        print("No recipes found with that ingredient.")
        return

    for row in matches:
        print("\n-------------------------")
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Ingredients: {row[2]}")
        print(f"Cooking Time: {row[3]} minutes")
        print(f"Difficulty: {row[4]}")
    print("-------------------------")


def update_recipe(conn, cursor):
    print("\n--- Update a Recipe ---")

    cursor.execute("SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes")
    recipes = cursor.fetchall()

    if not recipes:
        print("No recipes available to update.")
        return

    print("\nRecipes:")
    for r in recipes:
        print(f"ID: {r[0]} | {r[1]} | {r[4]}")

    try:
        recipe_id = int(input("\nEnter the ID of the recipe to update: ").strip())
    except ValueError:
        print("Invalid ID.")
        return

    # Verify recipe exists
    cursor.execute("SELECT id, name, ingredients, cooking_time FROM Recipes WHERE id = %s", (recipe_id,))
    current = cursor.fetchone()
    if not current:
        print("No recipe found with that ID.")
        return

    print("\nWhich field do you want to update?")
    print("1. name")
    print("2. cooking_time")
    print("3. ingredients")
    choice = input("Enter 1/2/3: ").strip()

    if choice == "1":
        new_name = input("New name: ").strip()
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_name, recipe_id))
        conn.commit()
        print("✅ Updated name.")

    elif choice == "2":
        try:
            new_time = int(input("New cooking time (minutes): ").strip())
        except ValueError:
            print("Invalid cooking time.")
            return

        # Need ingredients to recalc difficulty
        cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        ing_str = cursor.fetchone()[0] or ""
        ingredients = [p.strip() for p in ing_str.split(",") if p.strip()]
        new_diff = calculate_difficulty(new_time, ingredients)

        cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_time, recipe_id))
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_diff, recipe_id))
        conn.commit()
        print("✅ Updated cooking_time (and difficulty).")

    elif choice == "3":
        ingredients = []
        print("Enter new ingredients one at a time. Type 'done' when finished.")
        while True:
            item = input("Ingredient: ").strip()
            if item.lower() == "done":
                break
            if item:
                ingredients.append(item)

        new_ing_str = ", ".join(ingredients)

        # Need cooking_time to recalc difficulty
        cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (recipe_id,))
        cooking_time = cursor.fetchone()[0]
        new_diff = calculate_difficulty(cooking_time, ingredients)

        cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (new_ing_str, recipe_id))
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_diff, recipe_id))
        conn.commit()
        print("✅ Updated ingredients (and difficulty).")

    else:
        print("Invalid choice.")


def delete_recipe(conn, cursor):
    print("\n--- Delete a Recipe ---")

    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()
    if not recipes:
        print("No recipes available to delete.")
        return

    print("\nRecipes:")
    for r in recipes:
        print(f"ID: {r[0]} | {r[1]}")

    try:
        recipe_id = int(input("\nEnter the ID of the recipe to delete: ").strip())
    except ValueError:
        print("Invalid ID.")
        return

    cursor.execute("SELECT id FROM Recipes WHERE id = %s", (recipe_id,))
    exists = cursor.fetchone()
    if not exists:
        print("No recipe found with that ID.")
        return

    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))
    conn.commit()
    print("✅ Recipe deleted.")


def main_menu(conn, cursor):
    while True:
        print("\n========== Recipe App (MySQL) ==========")
        print("1. Create a recipe")
        print("2. Search for recipes by ingredient")
        print("3. Update a recipe")
        print("4. Delete a recipe")
        print("5. Quit")
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Part 1: Create & Connect Database
    conn = mysql.connector.connect(
        host="localhost",
        user="cf-python",
        passwd="password",
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
    cursor.execute("USE task_database")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Recipes (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50),
            ingredients VARCHAR(255),
            cooking_time INT,
            difficulty VARCHAR(20)
        )
        """
    )

    main_menu(conn, cursor)