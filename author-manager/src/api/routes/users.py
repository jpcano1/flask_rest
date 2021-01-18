from flask import Blueprint, request
from ..utils import (response_with, db,
                     generate_verification_token,
                     confirm_verification_token)
from ..utils import responses as resp
from ..models import User, UserSchema
from flask_jwt_extended import create_access_token
import sys

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        data["password"] = User.generate_hash(data["password"])
        user_schema = UserSchema()
        user = user_schema.load(data, session=db.session)
        user_schema.dump(user.create())
        return response_with(resp.SUCCESS_200)
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422, value={
            "error_message": str(e)
        })

@user_routes.route("/login", methods=["POST"])
def authenticate_user():
    try:
        data = request.get_json()
        current_user = None
        if data.get("username"):
            current_user = User.find_by_username(data["username"])
        elif data.get("email"):
            current_user = User.fin_by_email(data["email"])

        if not current_user:
            return response_with(resp.INVALID_INPUT_422, value={
                "message": "Wrong email or password"
            })
        if current_user and not current_user.is_verified:
            return response_with(resp.UNAUTHORIZED_401, value={
                "message": "You are not verified"
            })
        verification = User.verify_hash(data["password"],
                                        current_user.password)
        if verification:
            access_token =  create_access_token(identity=data["username"])
            return response_with(resp.SUCCESS_201, value={
                "message": f"Logged in as {current_user.username}",
                "access_token": access_token
            })
        else:
            return response_with(resp.UNAUTHORIZED_401, value={
                "message": "Wrong email or password"
            })
    except Exception as e:
        print(e, file=sys.stderr)
        return response_with(resp.INVALID_INPUT_422)

@user_routes.route("/confirm/<token>", methods=["POST"])
def verify_email(token):
    try:
        email = confirm_verification_token(token)
    except Exception as e:
        print(e, file=sys.stderr)
        return response_with(resp.UNAUTHORIZED_401)
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_verified:
        return response_with(resp.INVALID_INPUT_422, value={
            "message": "You are already verified"
        })
    else:
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        return response_with(resp.SUCCESS_200, value={
            "message": "E-mail verified, you can proceed to login now"
        })