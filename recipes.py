from db import db

import users


def enter(recipe_name, description, portions, instructions, items):
    user_id = users.user_id()

    try:
        sql = "INSERT INTO recipes (name, description, instructions, portions, created_at, user_id, visible) VALUES \
            (:name, :description, :instructions, :portions, NOW(), :user_id, 1)"
        db.session.execute(sql, {"name": recipe_name, "description": description,
                           "instructions": instructions, "portions": portions, "user_id": user_id})
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
            db.session.execute(sql, {
                               "ingredient": ingredient, "amount": amount, "unit": unit, "recipe_id": recipe_id})
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
    #sql = "SELECT R.*, CONCAT('/recipe/', R.id), U.username FROM recipes R, users U WHERE R.user_id=U.id"
    sql = "SELECT R.id, R.name, R.instructions, R.portions, R.created_at, R.user_id, CONCAT('/recipe/', R.id), U.username, R.description, \
        (SELECT COALESCE(AVG(rating), 0) FROM ratings WHERE recipe_id=R.id) AS stars, R.views, U.id \
        FROM recipes R, users U WHERE R.user_id=U.id"

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
    sql = "SELECT R.id, R.name, R.instructions, R.portions, R.created_at, R.user_id, R.description FROM recipes R WHERE R.id=:id"
    result = db.session.execute(sql, {"id": recipe_id})
    return result.fetchone()


def get_ingredients_by_id(recipe_id):
    sql = "SELECT * FROM ingredients WHERE recipe_id=:recipe_id"
    result = db.session.execute(sql, {"recipe_id": recipe_id})
    return result.fetchall()


def made_by_user(user_id):
    sql = "SELECT R.id, R.name, R.instructions, R.portions, R.created_at, R.user_id, CONCAT('/recipe/', R.id), R.description FROM recipes R WHERE R.user_id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()


def add_grading(recipe_id, user_id, grade):
    try:
        sql = "INSERT INTO ratings (recipe_id, user_id, rating, created_at) VALUES (:recipe_id, :user_id, :rating, NOW())"
        db.session.execute(
            sql, {"recipe_id": recipe_id, "user_id": user_id, "rating": grade})
        db.session.commit()
    except:
        return False


def find_recipes(search_string):
    """Search for matches in recipe names and then return the details"""

    # if the search string is empty, return all recipes
    if not search_string:
        return list_recipes()

    search_string = "%" + search_string + "%"
    sql = "SELECT R.id, R.name, R.instructions, R.portions, R.created_at, R.user_id, CONCAT('/recipe/', R.id), U.username, R.description FROM recipes R, users U WHERE R.user_id=U.id AND R.name ILIKE :search_string"
    result = db.session.execute(sql, {"search_string": search_string})
    return result.fetchall()


def count_rating(recipe_id):
    sql = "SELECT COALESCE(AVG(rating), 0) FROM ratings WHERE recipe_id=:recipe_id"
    result = db.session.execute(sql, {"recipe_id": recipe_id})
    retult = result.fetchone()
    print(result)
    return result


def add_view(recipe_id):
    sql = "UPDATE recipes SET views = views+1 WHERE id=:recipe_id"
    db.session.execute(sql, {"recipe_id": recipe_id})
    db.session.commit()


def sort_recipes(method):
    # value=1 Uusin ensin
    # value=2 Vanhin ensin
    # value=3 Parhaiten arvioitu ensin
    # value=4 Huonoiten arvioitu ensin
    # value=5 Eniten katseluja ensin
    # value=6 Vähiten katseluja ensin

    options = {"1": " ORDER BY R.created_at DESC, R.name ASC",
               "2": " ORDER BY R.created_at ASC, R.name ASC",
               "3": " ORDER BY stars DESC, R.name ASC",
               "4": " ORDER BY stars ASC, R.name ASC",
               "5": " ORDER BY R.views DESC, R.name ASC",
               "6": " ORDER BY R.views ASC, R.name ASC"}

    sql = "SELECT R.id, R.name, R.instructions, R.portions, R.created_at, R.user_id, CONCAT('/recipe/', R.id), U.username, R.description, \
        (SELECT COALESCE(AVG(rating), 0) FROM ratings WHERE recipe_id=R.id) AS stars, R.views \
        FROM recipes R, users U WHERE R.user_id=U.id"
    sql = sql + options[method]
    result = db.session.execute(sql)
    return result.fetchall()


def modify(recipe_id, recipe_name, description, portions, instructions, items):
    
    try:
        sql = "UPDATE recipes SET name=:name, description=:description, instructions=:instructions, portions=:portions, created_at=NOW() \
            WHERE id=:recipe_id"
        db.session.execute(sql, {"name": recipe_name, "description": description,
                            "instructions": instructions, "portions": portions, "recipe_id": recipe_id})
        db.session.commit()
    except:
        return False

    try:
        # first delete old records
        sql = "DELETE FROM ingredients WHERE recipe_id=:recipe_id"
        db.session.execute(sql, {"recipe_id": recipe_id})
        db.session.commit()
        # then insert the modified versions
        for item in items:
            # unpack values
            ingredient, amount, unit = item
            sql = "INSERT INTO ingredients (name, amount, unit, recipe_id) VALUES (:ingredient, :amount, :unit, :recipe_id)"
            db.session.execute(sql, {
                               "ingredient": ingredient, "amount": amount, "unit": unit, "recipe_id": recipe_id})
            db.session.commit()
    except:
        return False
    return True
