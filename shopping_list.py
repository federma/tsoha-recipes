from db import db

import users, recipes

def is_in_list(cart_id, user_id, recipe_id):
    """Check if recipe is already in users cart. Returns boolean."""

    sql = "SELECT 1 FROM shopping_list WHERE cart_id=:cart_id AND user_id=:user_id AND recipe_id=:recipe_id"
    result = db.session.execute(sql, {"cart_id": cart_id, "user_id": user_id, "recipe_id": recipe_id})
    return result.fetchone() != None


def add_recipe(cart_id, user_id, recipe_id):
    """add recipe to shopping list"""

    if is_in_list(cart_id, user_id, recipe_id):
        # block double entry
        return True

    try:
        sql = "INSERT INTO shopping_list (cart_id, user_id, recipe_id, inserted_at) VALUES \
            (:cart_id, :user_id, :recipe_id, NOW())"
        db.session.execute(sql, {"cart_id": cart_id, "user_id": user_id, "recipe_id": recipe_id})
        db.session.commit()
        return True
    except:
        return False


def remove_recipe(cart_id, user_id, recipe_id):
    """remove recipe from shopping list"""

    try:
        print("yritetään poistaa ", cart_id, user_id, recipe_id)
        sql = "DELETE FROM shopping_list WHERE cart_id=:cart_id AND user_id=:user_id AND recipe_id=:recipe_id"
        db.session.execute(sql, {"cart_id": cart_id, "user_id": user_id, "recipe_id": recipe_id})
        db.session.commit()
        print("poisto onnistui")
        return True
    except:
        return False


def generate_list(cart_id, user_id, portions):
    """returns a dictionary with recipe-id as key and ingredients as values (as immutable dict)"""

    # first get the recipes
    result = {}
    try:
        sql = "SELECT recipe_id FROM shopping_list WHERE cart_id=:cart_id AND user_id=:user_id"
        recipe_ids = db.session.execute(sql, {"cart_id": cart_id, "user_id": user_id})
        recipe_ids = recipe_ids.fetchall()
    except:
        return False

    for id in recipe_ids:
        id = id[0]
        name = recipes.get_details_by_id(id)[1]
        ingredients = recipes.get_ingredients_by_id_and_portions(id, portions)
        result[name] = ingredients

    return result   
    

def clear_cart(cart_id, user_id):
    """removes all items in the cart"""

    try:
        sql = "DELETE FROM shopping_list WHERE cart_id=:cart_id AND user_id=:user_id"
        db.session.execute(sql, {"cart_id": cart_id, "user_id": user_id})
        db.session.commit()
    except:
        return False


    