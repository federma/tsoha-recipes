from db import db

import users

def enter(recipe_name, instructions, item1, item2, item3):
    user_id = users.user_id()
    try:
        sql = "INSERT INTO recipes (name, instructions, created_at, user_id) VALUES (:name, :instructions, NOW(), :user_id)"
        db.session.execute(sql, {"name": recipe_name, "instructions": instructions, "user_id": user_id})
        db.session.commit()
    except:
        return False
    try:
        recipe_id = get_recipe_id(recipe_name)
        items = [item1, item2, item3]
        # atm this can fail for some particular item and then recipe/ingredients would be inserted only partially, needs a fix later
        for item in items:
            unit = "g"
            sql = "INSERT INTO ingredients (name, amount, unit, recipe_id) VALUES (:item, 42, :unit, :recipe_id)"
            db.session.execute(sql, {"item": item, "unit": unit, "recipe_id": recipe_id})
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
    sql = "SELECT * FROM recipes"
    result = db.session.execute(sql)
    return result.fetchall()
        