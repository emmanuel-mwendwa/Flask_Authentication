from flask import Blueprint, jsonify, request

from app.auth.views import token_auth

from ..models import User, Permission
from ..decorators import permission_required
from .. import db

main = Blueprint("main", __name__)

class UserRoutes:
    @main.post("/users")
    def users():
        data = request.get_json()
        new_user = User(
            username = data.get("username"),
            email = data.get("email"),
            password = data.get("password")
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": [
            {"data": "User added successfully"},
            {"user": new_user.to_json()}
        ]})
    
    @main.get("/users")
    @token_auth.login_required
    @permission_required(Permission.VIEW)
    def view_users():
        users = User.query.all()
        users_list = []

        for user in users:
            users_list.append(user.to_json())
        return jsonify({"Users": users_list})
    
    @main.get("/users/<int:id>")
    @token_auth.login_required
    @permission_required(Permission.VIEW)
    def view_user(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"})
        return jsonify(user.to_json())
    
    @main.put("/users/<int:id>")
    @token_auth.login_required
    @permission_required(Permission.MODERATE)
    def update_user(id):
        data = request.get_json()
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"})
        
        user.username = data.get("username")
        user.email = data.get("email")

        return jsonify({"message": [
            {"data": "User updated successfully"},
            {"user": user.to_json()}
        ]})
    
    @main.delete("/users/<int:id>")
    @token_auth.login_required
    @permission_required(Permission.ADMIN)
    def delete_user(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"})
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    
    