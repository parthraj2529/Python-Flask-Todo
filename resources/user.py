from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.user import UserModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import UserSchema
from flask import jsonify
from passlib.hash import pbkdf2_sha256

blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        if not users:
            return jsonify({"message": "No users found"}), 200
        return users

@blp.route("/user/register")
class UserRegister(MethodView):
    
    @blp.arguments(UserSchema)
    @blp.response(201, description="User created successfully")
    def post(self, user_data):
        try:
            user = UserModel(
                username = user_data["username"],
                password=pbkdf2_sha256.hash(user_data["password"])
            )
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An item with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return jsonify({
            "message": "User created successfully",
            "user": UserSchema().dump(user)  # Serialize the user object
        }), 

# @blp.route("/user/login")
# class UserLogin(MethodView):
#     @blp.arguments(UserSchema)
#     def post(self, user_data):
#         user = UserModel.query.filter(UserModel.username == user_data["username"])
     