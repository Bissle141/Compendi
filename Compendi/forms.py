from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, RadioField, BooleanField, EmailField
from wtforms.fields import FormField, FieldList
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo, Email


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=255)])
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")
    
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=255)])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    password_confirm = PasswordField("Confirm Password", validators= [EqualTo('password', message='Paswords must match')])
    submit = SubmitField("Register")
    
class ProjectCreationForm(FlaskForm):
    project_name = StringField('project_name', validators=[DataRequired(),Length(min=4, max=255)])
    desc = TextAreaField('desc', validators=[Length(max=255)])
    submit = SubmitField("Create")

class FolderFileCreationForm(FlaskForm):
    type_selection = RadioField('type_selection', choices=[('folder', 'Folder'), ('file', 'File')])
    name = StringField("name", validators=[InputRequired(), Length(max=100, min=4)]) 
    submit = SubmitField("Create")

class FileSectionForm(FlaskForm):
    header = StringField("Section Header", validators= [DataRequired(),Length(min=4, max=100)])
    body = TextAreaField('Section Body', validators=[Length(max=5000)])

class FileImageForm(FlaskForm):
    pass
    
class FileMainForm(FlaskForm):
    name = StringField("File Name", validators= [DataRequired(),Length(min=4, max=100)])
    sub = StringField("File Name", validators= [DataRequired(),Length(min=4, max=100)])
    sections = FieldList(FormField(FileSectionForm), min_entries=1)
    submit = SubmitField('Create')
