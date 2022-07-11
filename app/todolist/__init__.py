from flask import Blueprint

bp = Blueprint('todolist', __name__)

from app.todolist import  routes