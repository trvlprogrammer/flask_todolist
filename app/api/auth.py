
from urllib import response
from app.api import bp
from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required, current_user
from app.models import User
from app import jwt, db
from app.models import TokenBlocklist
from datetime import timedelta, timezone, datetime
from app import api_response
from app.utils import mail

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None

@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Username or password invalid"}), 401
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    return jsonify(access_token=access_token,refresh_token=refresh_token)

@bp.route("/register", methods=["POST"])
def register():
    try:        
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        email = request.json.get("email", None)
        if not username or not email or not password:
            return api_response("error","Must include username, email and password fields",{})
        if User.query.filter_by(username=username).first():
            return api_response("error","Please use a different username",{})
        if User.query.filter_by(email=email).first():
            return api_response("error","Please use a different email address",{})
        user = User(username=username,email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return api_response("success","User has been registered",{})
    except Exception as e:
        return api_response("error","Error register user",{})

@bp.route("/logout", methods=["DELETE"])
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify(msg="JWT revoked")


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    email = request.json.get("email", None)
    
    user = User.query.filter_by(email=email).first()
    if user:
        mail.send_password_reset_email(user)
        return api_response("success","Please check your email",{})
    return api_response("error","Email not found",{})

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    password = request.json.get("password", None)
    user = User.verify_reset_password_token(token)
    if not user:
        return api_response("error","user not fouund",{})

    user.set_password(password)
    db.session.commit()
    return api_response("success","Password updated!",{})