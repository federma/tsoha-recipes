from werkzeug.security import check_password_hash
from app import app
from flask import render_template, request, redirect
import users, recipes

@app.route("/")
def index():
    #todo front page with buttons (login, recipes, make a shopping list)
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti epäonnistui")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/new_recipe", methods=["GET", "POST"])
def new_recipe():
    if request.method == "GET":
        return render_template("add_recipe.html")
    if request.method == "POST":
        recipe_name = request.form["recipe_name"]
        instructions = request.form["instructions"]
        item1 = request.form["item1"]
        item2 = request.form["item2"]
        item3 = request.form["item3"]

        if recipes.enter(recipe_name, instructions, item1, item2, item3):
            return redirect("/")
        else:
            return render_template("error.html", message="Reseptin lisääminen epäonnistui")

@app.route("/recipes")
def recipes_show():
    list_of_recipes = recipes.list_recipes()
    print(list_of_recipes)
    return render_template("show_recipes.html", all_recipes = list_of_recipes)

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    recipe_details = recipes.get_details_by_id(recipe_id)
    print(recipe_details)
    ingredients = recipes.get_ingredients_by_id(recipe_id)
    print(ingredients)
    return render_template("recipe.html", details=recipe_details, ingredients=ingredients)