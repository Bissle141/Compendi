from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Users(db.Model):
    '''Users Table'''
    
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(999), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)

    ### RELATIONSHIPS
    projects = db.relationship('Projects', back_populates='user')

    ### FUNCTIONS
    def __repr__(self):
        return f"<{self.username}, user_id={self.user_id}, email={self.email}, joined={self.created}>"
    
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        self.created = datetime.now()
        
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

class Projects(db.Model):
    '''Projects Table'''
    
    __tablename__ = "projects"

    project_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    desc = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, default=datetime.now)
    
    ### FOREIGN KEYS
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    root_folder_id = db.Column(db.Integer, db.ForeignKey('folders.folder_id'), nullable=True)
        
    ### RELATIONSHIPS 
    user = db.relationship('Users', back_populates='projects')
    # folders = db.relationship('Folders', back_populates='project')

    def __repr__(self):
        return f"<{self.name}, project_id={self.project_id}, desc={self.desc}, created={self.created}>"
    
    def __init__(self, name, desc, user_id):      
        self.name = name
        self.desc = desc
        self.created = datetime.now()
        self.user_id = user_id
    
    def create_root(self):
        root_folder = Folders('', True, self.project_id)
        db.session.add(root_folder)
        db.session.commit()
        
        self.root_folder_id = root_folder.folder_id
        
class Folders(db.Model):
    '''Folders Table'''
    
    __tablename__ = "folders"

    folder_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    is_root = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)
    
    ### FOREIGN KEYS
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    parent_folder_id = db.Column(db.Integer, db.ForeignKey('folders.folder_id'), nullable=True)

    ### RELATIONSHIPS 
    # project = db.relationship("Projects", back_populates='folders')
    # files = db.relationship("Files", back_populates='folder_files')

    def __repr__(self):
        return f"<{self.name}, folder_id={self.folder_id}, is_root={self.is_root}, created={self.created}>"
    
    def __init__(self, name, is_root, project_id, parent_folder_id=None):
        if is_root is True:
            self.name = 'root_folder'
        else:
            self.name = name
        
        self.is_root = is_root
        self.created = datetime.now()
        
        self.project_id = project_id
        self.parent_folder_id = parent_folder_id
        
    def create_child_file(self, name):
        return Files(name, self.project_id, self.folder_id)
    
    def get_parent_folder(self):
        return Folders.query.get(self.parent_folder_id)

    ######### Whenever creating a file use this method on the parent folder instead of init
    def create_child_folder(self,name):
        return Folders(name=name, is_root=False, project_id=self.project_id, parent_folder_id=self.folder_id)
        
class Files(db.Model):
    '''Files Table'''
    
    __tablename__ = "files"


    file_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)
    
    ### FOREIGN KEYS
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    parent_folder_id = db.Column(db.Integer, db.ForeignKey('folders.folder_id'), nullable=True)

    ### RELATIONSHIPS 
    # project = db.relationship("Projects", back_populates='files_project')
    # images = db.relationship("Images", back_populates='file_images')
    # sections = db.relationship("Sections", back_populates='file_sections')

    def __repr__(self):
        return f"<{self.name}, project_id={self.files_id}, created={self.created}>"
    
    def __init__(self, name, project_id, parent_folder_id=None):
        self.name = name
        self.created = datetime.now()
        self.project_id = project_id
        self.parent_folder_id = parent_folder_id
        
class Images(db.Model):
    '''Images Table'''
    
    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    public_id = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)

    ### FOREIGN KEYS
    file_id = db.Column(db.Integer, db.ForeignKey('files.file_id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    
    ### RELATIONSHIPS
    # File = db.relationship("Files", back_populates='images_file')

    def __repr__(self):
        return f"<image_id={self.image_id}, public_id={self.public_id}>"
    
    def __init__(self, public_id, file_id, project_id):
        self.public_id = public_id
        self.created = datetime.now()
        self.file_id = file_id
        self.project_id = project_id

class Sections(db.Model):
    '''Sections Table'''
    
    __tablename__ = "sections"

    section_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    header = db.Column(db.String(255), nullable=False)
    sub_header = db.Column(db.String(255), default='')
    body = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)
    last_updated = db.Column(db.DateTime, default=datetime.now)
    
    ### FOREIGN KEYS
    file_id = db.Column(db.Integer, db.ForeignKey('files.file_id', ondelete='CASCADE'), nullable=False)

    ### RELATIONSHIPS
    # File = db.relationship('Files', back_populates='section_file')

    def __repr__(self):
        return f"<{self.header}, section_id={self.section_id}, created={self.created}, last_updated={self.last_updated}>"
    
    def __init__(self, header, sub_header, body, file_id):
        self.header = header
        self.sub_header = sub_header
        self.body = body
        self.created = datetime.now()
        self.last_updated = datetime.now()
        self.file_id = file_id


def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.app = app
    db.init_app(app)
    
if __name__ == '__main__':
    app = Flask(__name__)
    connect_to_db(app)
    print('Connected to db!')