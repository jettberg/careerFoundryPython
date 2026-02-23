"""
recipe_app.py — Final CLI Recipe App (Exercise 1.7)

Uses SQLAlchemy ORM + MySQL to:
1) Create recipes
2) View recipes
3) Search by ingredients
4) Edit a recipe
5) Delete a recipe

Notes:
- Ingredients are stored as a single comma+space separated string (", ")
- Difficulty is calculated and stored automatically
"""

from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# -----------------------------
# SQLAlchemy Setup
# -----------------------------
DB_USER = "cf-python"
DB_PASS = "password"
DB_HOST = "localhost"
DB_NAME = "task_database"  # per instructions, you can reuse task_database

# IMPORTANT:
# mysql+mysqlconnector requires mysql-connector-python installed.
ENGINE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(ENGINE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


# -----------------------------
# Model
# -----------------------------
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))  # stored as "Milk, Sugar, ..."
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe(id={self.id}, name='{self.name}', difficulty='{self.difficulty}')>"

    def __str__(self):
        # pretty output for the CLI
        line = "-" * 35
        ing_list = self.return_ingredients_as_list()
        ing_display = "\n".join([f"  - {i}" for i in ing_list]) if ing_list else "  (none)"

        return (
            f"\n{line}\n"
            f"Recipe ID:\t{self.id}\n"
            f"Name:\t\t{self.name}\n"
            f"Cooking Time:\t{self.cooking_time} min\n"
            f"Difficulty:\t{self.difficulty}\n"
            f"Ingredients:\n{ing_display}\n"
            f"{line}\n"
        )

    def calculate_difficulty(self):
        ing_count = len(self.return_ingredients_as_list())
        ct = self.cooking_time if self.cooking_time is not None else 0

        if ct < 10 and ing_count < 4:
            self.difficulty = "Easy"
        elif ct < 10 and ing_count >= 4:
            self.difficulty = "Medium"
        elif ct >= 10 and ing_count < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        # split exactly on comma+space to match how we join
        return self.ingredients.split(", ")


# Create the table if it doesn't exist
Base.metadata.create_all(engine)


# -----------------------------
# Helpers for safe input
# -----------------------------
def prompt_nonempty(prompt_text: str, max_len: int | None = None) -> str:
    while True:
        val = input(prompt_text).strip()
        if not val:
            print("Please enter something (not empty).")
            continue
        if max_len is not None and len(val) > max_len:
            print(f"Too long. Max length is {max_len}. Try again.")
            continue
        return val


def prompt_int(prompt_text: str, min_value: int | None = None) -> int:
    while True:
        raw = input(prompt_text).strip()
        if not raw.isnumeric():
            print("Please enter a valid number (digits only).")
            continue
        num = int(raw)
        if min_value is not None and num < min_value:
            print(f"Please enter a number >= {min_value}.")
            continue
        return num


# -----------------------------
# Function 1: create_recipe()
# -----------------------------
def create_recipe():
    print("\n--- Create a New Recipe ---")
    name = prompt_nonempty("Recipe name (max 50 chars): ", max_len=50)
    cooking_time = prompt_int("Cooking time in minutes: ", min_value=0)

    ingredients_temp: list[str] = []
    count = prompt_int("How many ingredients do you want to enter? ", min_value=0)

    for i in range(count):
        ing = prompt_nonempty(f"Ingredient {i+1}: ", max_len=50)
        ingredients_temp.append(ing)

    # Join list into a single string
    ingredients_str = ", ".join(ingredients_temp)

    recipe_entry = Recipe(
        name=name,
        cooking_time=cooking_time,
        ingredients=ingredients_str,
    )
    recipe_entry.calculate_difficulty()

    session.add(recipe_entry)
    session.commit()

    print("\nSaved! Here’s what you added:")
    print(recipe_entry)


# -----------------------------
# Function 2: view_all_recipes()
# -----------------------------
def view_all_recipes():
    print("\n--- View All Recipes ---")
    recipes = session.query(Recipe).all()

    if not recipes:
        print("No recipes found yet.")
        return None

    for r in recipes:
        print(r)


# -----------------------------
# Function 3: search_by_ingredients()
# -----------------------------
def search_by_ingredients():
    print("\n--- Search Recipes by Ingredients ---")

    if session.query(Recipe).count() == 0:
        print("No recipes exist yet. Add some first.")
        return None

    # Get ingredients column only
    results = session.query(Recipe.ingredients).all()

    all_ingredients: list[str] = []
    for (ing_str,) in results:
        if not ing_str:
            continue
        temp_list = ing_str.split(", ")
        for ing in temp_list:
            if ing not in all_ingredients:
                all_ingredients.append(ing)

    if not all_ingredients:
        print("No ingredients found in the database yet.")
        return None

    # Display numbered list
    print("\nAvailable ingredients:")
    for idx, ing in enumerate(all_ingredients, start=1):
        print(f"{idx}. {ing}")

    raw = input("\nType ingredient number(s) separated by spaces (example: 1 3 5): ").strip()
    if not raw:
        print("No selection made. Returning to menu.")
        return None

    tokens = raw.split()
    if not all(t.isnumeric() for t in tokens):
        print("Invalid input. Please enter numbers only.")
        return None

    nums = [int(t) for t in tokens]
    if any(n < 1 or n > len(all_ingredients) for n in nums):
        print("One or more numbers were out of range.")
        return None

    search_ingredients = [all_ingredients[n - 1] for n in nums]

    # Build conditions list
    conditions = []
    for ing in search_ingredients:
        like_term = f"%{ing}%"
        conditions.append(Recipe.ingredients.like(like_term))

    matches = session.query(Recipe).filter(*conditions).all()

    if not matches:
        print("\nNo recipes matched your ingredient selection.")
        return None

    print("\nMatches found:")
    for r in matches:
        print(r)


# -----------------------------
# Function 4: edit_recipe()
# -----------------------------
def edit_recipe():
    print("\n--- Edit a Recipe ---")

    if session.query(Recipe).count() == 0:
        print("No recipes exist yet.")
        return None

    results = session.query(Recipe.id, Recipe.name).all()
    print("\nRecipes available:")
    for rid, name in results:
        print(f"ID {rid}: {name}")

    chosen_id = prompt_int("\nEnter the ID of the recipe you want to edit: ", min_value=1)

    recipe_to_edit = session.query(Recipe).filter(Recipe.id == chosen_id).one_or_none()
    if recipe_to_edit is None:
        print("That ID does not exist. Returning to menu.")
        return None

    print("\nCurrent recipe:")
    print(f"1) Name:         {recipe_to_edit.name}")
    print(f"2) Ingredients:  {recipe_to_edit.ingredients}")
    print(f"3) Cooking time: {recipe_to_edit.cooking_time}")

    choice = prompt_int("\nWhich field do you want to edit? (1-3): ", min_value=1)
    if choice not in (1, 2, 3):
        print("Invalid choice. Returning to menu.")
        return None

    if choice == 1:
        new_name = prompt_nonempty("New name (max 50 chars): ", max_len=50)
        recipe_to_edit.name = new_name

    elif choice == 2:
        # Re-enter ingredients the same way as create
        ingredients_temp: list[str] = []
        count = prompt_int("How many ingredients do you want to enter now? ", min_value=0)
        for i in range(count):
            ing = prompt_nonempty(f"Ingredient {i+1}: ", max_len=50)
            ingredients_temp.append(ing)
        recipe_to_edit.ingredients = ", ".join(ingredients_temp)

    elif choice == 3:
        new_time = prompt_int("New cooking time (minutes): ", min_value=0)
        recipe_to_edit.cooking_time = new_time

    # Recalculate difficulty after edits
    recipe_to_edit.calculate_difficulty()
    session.commit()

    print("\nUpdated recipe:")
    print(recipe_to_edit)


# -----------------------------
# Function 5: delete_recipe()
# -----------------------------
def delete_recipe():
    print("\n--- Delete a Recipe ---")

    if session.query(Recipe).count() == 0:
        print("No recipes exist yet.")
        return None

    results = session.query(Recipe.id, Recipe.name).all()
    print("\nRecipes available:")
    for rid, name in results:
        print(f"ID {rid}: {name}")

    chosen_id = prompt_int("\nEnter the ID of the recipe you want to delete: ", min_value=1)

    recipe_to_delete = session.query(Recipe).filter(Recipe.id == chosen_id).one_or_none()
    if recipe_to_delete is None:
        print("That ID does not exist. Returning to menu.")
        return None

    confirm = input(f"Are you sure you want to delete '{recipe_to_delete.name}'? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Delete cancelled.")
        return None

    session.delete(recipe_to_delete)
    session.commit()
    print("Deleted successfully.")


# -----------------------------
# Main Menu
# -----------------------------
def main_menu():
    while True:
        print("\n=== Recipe App ===")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("Type 'quit' to quit")

        choice = input("\nYour choice: ").strip().lower()

        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "quit":
            print("\nGoodbye!")
            break
        else:
            print("Invalid input. Please choose 1-5 or type 'quit'.")


if __name__ == "__main__":
    try:
        main_menu()
    finally:
        # Always close cleanly
        session.close()
        engine.dispose()