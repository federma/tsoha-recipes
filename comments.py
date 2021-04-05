from db import db
import users, recipes

def add_comment(comment, recipe_id):
    """Add new comment for a recipe"""
    user_id = users.user_id()
    try:
        sql = "INSERT INTO comments (comment, sent_at, user_id, recipe_id) VALUES (:comment, NOW(), :user_id, :recipe_id)"
        db.session.execute(sql, {"comment": comment, "user_id": user_id, "recipe_id": recipe_id})
        db.session.commit()
        return True
    except:
        return False

def get_comments(recipe_id):
    """Get all comments for a recipe-id sorted from latest to oldest"""
    sql = "SELECT C.*, U.username FROM comments C, users U WHERE C.recipe_id=:recipe_id AND C.user_id=U.id ORDER BY C.sent_at DESC"
    result = db.session.execute(sql, {"recipe_id": recipe_id})
    return result.fetchall()
    