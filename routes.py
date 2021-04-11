from werkzeug.security import check_password_hash
from app import app
from flask import render_template, request, redirect
import users
import recipes
import comments


@app.route("/")
def index():
    # current front page just has some info about the app, will need some more content or maybe I'll just drop this page
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
            return redirect("/profile")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/profile")


@app.route("/new_recipe", methods=["GET", "POST"])
def new_recipe():
    if request.method == "GET":
        return render_template("add_recipe.html")
    if request.method == "POST":
        form = request.form
        print(form)
        recipe_name = form["recipe_name"]
        portions = int(form["portions"])
        instructions = form["instructions"]
        items = zip(form.getlist("ingredient"), map(
            int, form.getlist("amount")), form.getlist("unit"))

        if recipes.enter(recipe_name, portions, instructions, items):
            return redirect("/recipes")
        else:
            return render_template("error.html", message="Reseptin lisääminen epäonnistui")


@app.route("/recipes")
def recipes_show():
    list_of_recipes = recipes.list_recipes()
    print(list_of_recipes)
    return render_template("show_recipes.html", all_recipes=list_of_recipes)


@app.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
def recipe(recipe_id):
    if request.method == "POST":
        comment = request.form["comment"]
        if not comments.add_comment(comment, recipe_id):
            return render_template("error.html", message="Kommentin lisääminen epäonnistui")

    recipe_details = recipes.get_details_by_id(recipe_id)
    print(recipe_details)
    ingredients = recipes.get_ingredients_by_id(recipe_id)
    print(ingredients)
    comment_list = comments.get_comments(recipe_id)
    return render_template("recipe.html", details=recipe_details, ingredients=ingredients, comment_list=comment_list)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        username = users.user_name()
        if not username:
            # user is not logged in, render log in option
            return render_template("profile.html", logged=username)
    # get all recipes made by current user
    users_recipes = recipes.made_by_user(users.user_id())
    return render_template("profile.html", logged=True, username=username, users_recipes=users_recipes)

        # if user is logging in, replaces old separate login page
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/profile")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

