from werkzeug.security import check_password_hash
from app import app
from flask import render_template, request, redirect
import users
import recipes
import comments
import shopping_list


@app.route("/")
def index():
    # front page, not much content - just some info about the app
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # register new users
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
    # login page
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
        recipe_name = form["recipe_name"]
        portions = int(form["portions"])
        description = form["description"]
        instructions = form["instructions"]
        items = zip(form.getlist("ingredient"), map(
            int, form.getlist("amount")), form.getlist("unit"))

        if recipes.enter(recipe_name, description, portions, instructions, items):
            return redirect("/recipes")
        else:
            return render_template("error.html", message="Reseptin lisääminen epäonnistui")


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
        # check if user wants to search of sort recipes
        choice = request.form["route"]

        if choice == "find_recipes":
            query = request.form["find_recipe"]
            sorting_method = request.form["sorting_method"]
            list_of_recipes = recipes.search_sort_recipes(query, sorting_method)
            count = len(list_of_recipes)
            return render_template("show_recipes.html", all_recipes=list_of_recipes, query=query, sorting_method=sorting_method, count=count)

        if choice == "sort_recipes":
            sorting_method = request.form["sorting_btn"]
            query = request.form["query"]
            list_of_recipes = recipes.search_sort_recipes(query, sorting_method)
            count = len(list_of_recipes)
            return render_template("show_recipes.html", all_recipes=list_of_recipes, query=query, sorting_method=sorting_method, count=count)


@app.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
def recipe(recipe_id):
    if request.method == "POST":
        comment = request.form["comment"]
        if not comments.add_comment(comment, recipe_id):
            return render_template("error.html", message="Kommentin lisääminen epäonnistui")
    #print(recipe_id)
    recipes.add_view(recipe_id)
    recipe_details = recipes.get_details_by_id(recipe_id)
    #print(recipe_details)
    ingredients = recipes.get_ingredients_by_id(recipe_id)
    #print(ingredients)
    comment_list = comments.get_comments(recipe_id)
    in_cart = shopping_list.is_in_list(1, users.user_id(), recipe_id)

    return render_template("recipe.html", details=recipe_details, ingredients=ingredients, comment_list=comment_list, in_cart=in_cart)

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

@app.route("/grade", methods=["POST"])
def grade():
    recipe_id = request.form["r_id"]
    recipe_grade = request.form["grade"]
    u_id = users.user_id()
    #print(recipe_id, recipe_grade, u_id)
    #todo add grading to db
    recipes.add_grading(recipe_id, u_id, recipe_grade)
    return redirect("/recipe/" + recipe_id)


# this route is obsolete, clean up later
# @app.route("/find_recipe", methods=["POST"])
# def find_recipe():
#     search_string = request.form["find_recipe"]
#     list_of_recipes = recipes.find_recipes(search_string)
#     return render_template("show_recipes.html", all_recipes=list_of_recipes)


# this route is obsolete, clean up later
# @app.route("/sort_recipes", methods=["POST"])
# def sort_recipes():
#     sorting_method = request.form["sorting_btn"]
#     print("saatu ", sorting_method)
#     print(type(sorting_method))
#     list_of_recipes = recipes.sort_recipes(sorting_method)
#     return render_template("show_recipes.html", all_recipes=list_of_recipes)


@app.route("/recipe/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):

    if request.method == "GET":
        recipe_details = recipes.get_details_by_id(recipe_id)
        ingredients = recipes.get_ingredients_by_id(recipe_id)
        return render_template("edit_recipe.html", details=recipe_details, ingredients=ingredients)

    if request.method == "POST":
        form = request.form
        recipe_name = form["recipe_name"]
        portions = int(form["portions"])
        description = form["description"]
        instructions = form["instructions"]
        items = zip(form.getlist("ingredient"), map(
            int, form.getlist("amount")), form.getlist("unit"))

        print(recipe_id, recipe_name, portions, description, instructions, items)
        print(type(recipe_id))

        if recipes.modify(recipe_id, recipe_name, description, portions, instructions, items):
            return redirect("/recipes")
        else:
            return render_template("error.html", message="Reseptin muokkaaminen epäonnistui")


@app.route("/shopping-list", methods=["GET", "POST"])
def shopping_cart():

    if request.method == "GET":
        # default to two portions
        items = shopping_list.generate_list(1, users.user_id(), 2)
        print("listalla ovat ", items)
        return render_template("shopping_list.html", items=items, portions=2)
    
    if request.method == "POST":

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
    recipe_id = request.form["recipe_id"]
    u_id = users.user_id()

    insert_or_remove = request.form["modify_shopping_cart"]

    if insert_or_remove == "insert":
        shopping_list.add_recipe(1, u_id, recipe_id)
    else:
        shopping_list.remove_recipe(1, u_id, recipe_id)

    return redirect("/recipe/" + recipe_id)
                
