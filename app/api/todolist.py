from urllib import response
from xmlrpc.client import boolean
from flask import current_app, jsonify, render_template, request, send_file
from app.api import bp
from flask_jwt_extended import jwt_required, current_user
from app.models import Post, Tag, User
from app import db, api_response
from datetime import datetime
from app.todolist.routes import export_todo_file, allowed_file
from app.utils import mail
from werkzeug.utils import secure_filename
import openpyxl

@bp.route("/todos", methods=["GET"])
@jwt_required()
def get_todos():    
    try :
        page = request.args.get('page', 1, type=int)
        active = eval(request.args.get('active'))
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        data = Post.to_collection_dict(Post.query.filter_by(author=current_user,active=active).order_by(Post.date_todo.asc()), page, per_page, 'api.get_todos',active=active)
        return api_response("success","Success get todolist", data)
    except Exception(e): 
        return api_response("error", "Error get data", {})

@bp.route("/tags", methods=["GET"])
@jwt_required()
def get_tags():    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        data = Tag.to_collection_dict(Tag.query.filter_by(tag_user=current_user), page, per_page, 'api.get_tags')
        return api_response("success","Success get todolist", data)
    except Exception(e): 
        return api_response("error", "Error get data", {})

@bp.route("/todos", methods=["POST"])
@jwt_required()
def create_todo():    
    try :
        body = request.json.get("body", None)
        tags = request.json.get("tags", None)
        date_todo = request.json.get("date_todo", None)
        date_todo_obj = datetime.strptime(date_todo, '%Y-%m-%d %H:%M:%S').utcnow()
        tag_ids = []
        for tag in tags:
            tag_ids.append(tag['id'])
        tags  = db.session.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        post = Post(body=body, tags=tags, date_todo= date_todo_obj,author=current_user)
        db.session.add(post)
        db.session.commit()
        return api_response("success","Success create todolist", {})
    except Exception(e):        
        return api_response("error", "Error create data", {}) 

@bp.route("/tags", methods=["POST"])
@jwt_required()
def create_tag():    
    try:
        name = request.json.get("name", None)
        tag = Tag(name=name,tag_user=current_user)
        db.session.add(tag)
        db.session.commit()
        return api_response("success","Success create tag", {})
    except Exception(e):
        return api_response("error","Failed create tag", {})

@bp.route("/todos/<todo_id>", methods=["DELETE"])
@jwt_required()
def delete_todo(todo_id):    
    try:
        Post.query.filter_by(id=todo_id).delete()
        db.session.commit()
        return api_response("success","Success delete todo", {})
    except Exception(e):
        return api_response("error","Failed delete todo", {})

@bp.route("/tags/<tag_id>", methods=["DELETE"])
@jwt_required()
def delete_tag(tag_id):    
    try:
        Tag.query.filter_by(id=tag_id).delete()
        db.session.commit()
        return api_response("success","Success delete tag", {})
    except Exception(e):
        return api_response("error","Failed delete tag", {})

@bp.route('/todos/set_active/<todo_id>/<active>', methods=['POST'])
@jwt_required()
def todo_active_inactive(todo_id,active):
    try:
        if eval(active):
            status = "Unarchive"
        else:
            status = "Archive"
        post = Post.query.get(todo_id)
        post.active = eval(active)
        db.session.commit()
        return api_response("success","Success %s todo"%(status), {})
    except Exception(e):
        return api_response("error","Failed %s todo"%(status), {})


@bp.route('/todo/export/<user_id>', methods=['GET'])
def export_todo(user_id):
    user = User.query.get(user_id)     
    file_path = export_todo_file(user)
    return send_file(file_path)


@bp.route('/todo/export_email/<user_id>', methods=['GET'])
def export_todo_email(user_id):
    user = User.query.get(user_id)      
    file_path = export_todo_file(user)           
    with current_app.open_resource(file_path) as fp:
        attachment = {
            'file_name' : 'todo_export.xlsx',
            'content_type' : 'file/xlsx',
            'data' : fp.read()
        }
    html_body = render_template('email/export_todo.html',user=user)
    mail.send_email('Export Todo', current_app.config['ADMINS'][0], [user.email], None, html_body,attachment)
    return api_response("success","Success export and send to email", {})

@bp.route('/todo/import', methods=['POST'])
def import_todo():
    if 'file' not in request.files:
        return api_response("error","Cannot find file", {})
    file = request.files['file']
    if file.filename == '':
        return api_response("error","File name cannot be blank", {})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
        file.save(file_path)
        wb_obj = openpyxl.load_workbook(file_path)
        ws = wb_obj.active
        data_cell = ws["A:B"]            
        i = 1
        while i < len(data_cell[0]):
            post = Post(body=data_cell[0][i].value,active=data_cell[1][i].value,author=current_user)
            db.session.add(post)
            db.session.commit()
            i += 1
        return api_response("success","Success import todo", {})
        