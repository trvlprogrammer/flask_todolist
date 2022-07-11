from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,SelectMultipleField,StringField,DateTimeLocalField,FileField
from app.models import Tag
from flask import render_template, current_app
from wtforms.validators import Optional
# app = create_app()
# tags = [(t.id, t.name) for t in Tag.query.all()]

class PostForm(FlaskForm):
    body = TextAreaField('Description',render_kw={"placeholder": "Todo"})
    tags = SelectMultipleField('Tags',render_kw={"placeholder": "Tags"},coerce=int,)     
    date_todo = DateTimeLocalField('Date', format='%Y-%m-%dT%H:%M',validators=[Optional()])
    submit = SubmitField('Submit')
   

    def set_choices(self,current_user):
        self.tags.choices = [(d.id, d.name) for d in current_user.tags.all()]

class TagForm(FlaskForm):
    name = StringField('Tag',render_kw={"placeholder": "Tag"})    
    submit = SubmitField('Submit')


class UploadForm(FlaskForm):
    file = FileField()
    submit = SubmitField('Import')

