from os import abort
from werkzeug.security import check_password_hash
from app import app
from flask import render_template, request, redirect, session, flash
import users
import recipes
import comments
import shopping_list
import secrets
import snippets


@app.route("/")
def index():
    # front page, not much content - just some info about the app
    if users.user_id():
        # bug fix, old logged-in users might have had just user_id saved in session
        # user_name and csrf_token were added later to the code - to avoid errors, add them on the front page if necessary
        if not session.get("user_name", 0):
            session["user_name"] = users.user_name()

        if not session.get("csrf_token", 0):
            session["csrf_token"] = secrets.token_hex(16)

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # register new users
    if request.method == "GET":
        return render_template("register.html", message="")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if len(username) < 3 or len(username) > 50:
            return render_template("register.html", message="Käyttätunnuksen pituuden tulee olla 3-50 merkkiä")

        if len(password) < 3 or len(password) > 1000:
            return render_template("register.html", message="Salasanan pituuden tulee olla 3-1000 merkkiä")

        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("register.html", message="Rekisteröinti epäonnistui. Käyttäjätunnus on varattu tai tapahtui odottamaton virhe")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/profile")


@app.route("/new_recipe", methods=["GET", "POST"])
def new_recipe():
    if request.method == "GET":
        return render_template("add_recipe.html", message="")

    if request.method == "POST":
        form = request.form

        if session["csrf_token"] != form["csrf_token"]:
            abort(403)

        recipe_name = form["recipe_name"]
        portions = int(form["portions"])
        description = form["description"]
        instructions = form["instructions"]
        ingredients = form.getlist("ingredient")
        amounts = form.getlist("amount")
        amounts = snippets.convert_to_int(amounts)
        units = form.getlist("unit")

        check_form = snippets.validate_recipe_form(
            recipe_name, description, instructions, ingredients, amounts)
        if check_form != "validation_ok":
            return render_template("add_recipe.html", message=check_form)

        items = zip(ingredients, amounts, units)

        if recipes.enter(recipe_name, description, portions, instructions, items):
            flash("Reseptin lisäys onnistui. Reseptisi on oheisessa listauksessa ylimpänä.")
            return redirect("/recipes")
        else:
            return render_template("add_recipe.html", message="Reseptin lisääminen epäonnistui. Tapahtui odottamaton virhe.")


@app.route("/recipe/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "GET":
        recipe_details = recipes.get_details_by_id(recipe_id)
        ingredients = recipes.get_ingredients_by_id(recipe_id)
        return render_template("edit_recipe.html", details=recipe_details, ingredients=ingredients, message="")

    if request.method == "POST":
        form = request.form

        if session["csrf_token"] != form["csrf_token"]:
            abort(403)

        recipe_name = form["recipe_name"]
        portions = int(form["portions"])
        description = form["description"]
        instructions = form["instructions"]
        ingredients = form.getlist("ingredient")
        amounts = form.getlist("amount")
        amounts = snippets.convert_to_int(amounts)
        units = form.getlist("unit")

        check_form = snippets.validate_recipe_form(
            recipe_name, description, instructions, ingredients, amounts)
        if check_form != "validation_ok":
            recipe_details = recipes.get_details_by_id(recipe_id)
            ingredients = recipes.get_ingredients_by_id(recipe_id)
            return render_template("edit_recipe.html", details=recipe_details, ingredients=ingredients, message=check_form+" Palautettu alkuperäiset tiedot, voit yrittää muokkausta muokkausta uudelleen")

        items = zip(ingredients, amounts, units)

        if recipes.modify(recipe_id, recipe_name, description, portions, instructions, items):
            flash("Reseptin muokkaus onnistui. Muokattu reseptisi on oheisessa listauksessa ylimpänä.")
            return redirect("/recipes")
        else:
            recipe_details = recipes.get_details_by_id(recipe_id)
            ingredients = recipes.get_ingredients_by_id(recipe_id)
            return render_template("edit_recipe", details=recipe_details, ingredients=ingredients, message="Odottamaton virhe, muokkaaminen epäonnistui. Palautettu alkuperäiset tiedot, voit yrittää muokkausta halutessasi uudelleen.")


@app.route("/recipes", methods=["GET", "POST"])
def recipes_show():
    if request.method == "GET":
        # just show all the recipes, sort from latest
        query = ""
        sorting_method = "1"
        list_of_recipes = recipes.search_sort_recipes(query, sorting_method)
        count = len(list_of_recipes)
        return render_template("show_recipes.html", all_recipes=list_of_recipes, query=query, sorting_method=sorting_method, count=count)

    if request.method == "POST":
        # check if user wants to search or sort recipes
        choice = request.form["route"]

        if choice == "find_recipes":
            query = request.form["find_recipe"]
            sorting_method = request.form["sorting_method"]
            list_of_recipes = recipes.search_sort_recipes(
                query, sorting_method)
            count = len(list_of_recipes)
            return render_template("show_recipes.html", all_recipes=list_of_recipes, query=query, sorting_method=sorting_method, count=count)

        if choice == "sort_recipes":
            sorting_method = request.form["sorting_btn"]
            query = request.form["query"]
            list_of_recipes = recipes.search_sort_recipes(
                query, sorting_method)
            count = len(list_of_recipes)
            return render_template("show_recipes.html", all_recipes=list_of_recipes, query=query, sorting_method=sorting_method, count=count)


@app.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
def recipe(recipe_id):
    recipe_details = recipes.get_details_by_id(recipe_id)
    ingredients = recipes.get_ingredients_by_id(recipe_id)
    in_cart = shopping_list.is_in_list(1, users.user_id(), recipe_id)
    comment_list = comments.get_comments(recipe_id)

    if request.method == "GET":
        # just refreshing page adds views
        # would be better to later limit this to count only logged in users and maybe limit max one new view per user per hour 
        recipes.add_view(recipe_id)
        return render_template("recipe.html", details=recipe_details, ingredients=ingredients, comment_list=comment_list, in_cart=in_cart, message="")

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        comment = request.form["comment"]

        if len(comment) > 1000:
            return render_template("recipe.html", details=recipe_details, ingredients=ingredients, comment_list=comment_list, in_cart=in_cart, message="Kommentin enimmäispituus on 1000 merkkiä.")

        if len(comment) == 0:
            return render_template("recipe.html", details=recipe_details, ingredients=ingredients, comment_list=comment_list, in_cart=in_cart, message="Et voi lisätä tyhjää kommenttia.")

        if not comments.add_comment(comment, recipe_id):
            return render_template("recipe.html", details=recipe_details, ingredients=ingredients, comment_list=comment_list, in_cart=in_cart, message="Kommentin lisäys epäonnistui. Tapahtui odottamaton virhe.")

        # new comment was added
        comment_list = comments.get_comments(recipe_id)
        return render_template("recipe.html", details=recipe_details, ingredients=ingredients, comment_list=comment_list, in_cart=in_cart)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        username = users.user_name()

        if not username:
            # user is not logged in, render log in option
            return render_template("profile.html", logged=username)
        # user is logged in, get all recipes made by current user
        users_recipes = recipes.made_by_user(users.user_id())
        return render_template("profile.html", logged=True, username=username, users_recipes=users_recipes)

    # if user is logging in, replaces old separate login page
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/profile")
        else:
            return render_template("profile.html", message="Väärä tunnus tai salasana")


@app.route("/grade", methods=["POST"])
def grade():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    recipe_id = request.form["r_id"]
    recipe_grade = request.form["grade"]
    u_id = users.user_id()
    recipes.add_grading(recipe_id, u_id, recipe_grade)
    return redirect("/recipe/" + recipe_id)


@app.route("/shopping-list", methods=["GET", "POST"])
def shopping_cart():
    if request.method == "GET":
        # default to two portions
        items = shopping_list.generate_list(1, users.user_id(), 2)
        return render_template("shopping_list.html", items=items, portions="2")

    if request.method == "POST":

        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        portions = request.form["old_value"]

        try:
            portions = request.form["portions_number"]
            items = shopping_list.generate_list(1, users.user_id(), portions)
            return render_template("shopping_list.html", items=items, portions=portions)
        except:
            pass

        action = request.form["modify_shopping_cart"]

        if action == "delete_all":
            shopping_list.clear_cart(1, users.user_id())
            return render_template("shopping_list.html", items=None, portions=portions)


@app.route("/shopping-list/edit", methods=["POST"])
def edit_shopping_list():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    recipe_id = request.form["recipe_id"]
    u_id = users.user_id()

    insert_or_remove = request.form["modify_shopping_cart"]

    if insert_or_remove == "insert":
        shopping_list.add_recipe(1, u_id, recipe_id)
    else:
        shopping_list.remove_recipe(1, u_id, recipe_id)

    return redirect("/recipe/" + recipe_id)
