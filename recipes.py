from db import db

import users

def enter(recipe_name, portions, instructions, items):
    user_id = users.user_id()

    try:
        sql = "INSERT INTO recipes (name, instructions, portions, created_at, user_id) VALUES (:name, :instructions, :portions, NOW(), :user_id)"
        db.session.execute(sql, {"name": recipe_name, "instructions": instructions, "portions":portions, "user_id": user_id})
        db.session.commit()
    except:
        return False

    try:
        recipe_id = get_recipe_id(recipe_name)

        # atm this can fail midway for some particular item and then recipe/ingredients would be inserted only partially - need to make all inserts in one transaction?
        for item in items:
            # unpack values
            print("tulin tänne ja itemina on ", item)
            ingredient, amount, unit = item
            sql = "INSERT INTO ingredients (name, amount, unit, recipe_id) VALUES (:ingredient, :amount, :unit, :recipe_id)"
            db.session.execute(sql, {"ingredient": ingredient, "amount":amount, "unit": unit, "recipe_id": recipe_id})
            db.session.commit()
    except:
        return False
    return True

def get_recipe_id(name):
    try:
        sql = "SELECT id FROM recipes WHERE name=:name"
        result = db.session.execute(sql, {"name": name})
        id = result.fetchone()[0]
        return id
    except:
        return False

def list_recipes():
    """Returns all details in the recipes table and also adds url fields and recipes creators name"""
    sql = "SELECT R.*, CONCAT('/recipe/', R.id), U.username FROM recipes R, users U WHERE R.user_id=U.id"
    result = db.session.execute(sql)
    return result.fetchall()

# this is not used anywhere atm -> possibly remove later
def list_ids_and_names():
    ids = []
    names = []
    sql = "SELECT id, name FROM recipes"
    result = db.session.execute(sql)
    id_name_all = result.fetchall()
    for id, name in id_name_all:
        ids.append(id)
        names.append(name)
    return ids, names

def get_details_by_id(recipe_id):
    sql = "SELECT * FROM recipes WHERE id=:id"
    result = db.session.execute(sql, {"id": recipe_id})
    return result.fetchone()

def get_ingredients_by_id(recipe_id):
    sql = "SELECT * FROM ingredients WHERE recipe_id=:recipe_id"
    result = db.session.execute(sql, {"recipe_id": recipe_id})
    return result.fetchall()

def made_by_user(user_id):
    sql = "SELECT *, CONCAT('/recipe/', id) FROM recipes WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()