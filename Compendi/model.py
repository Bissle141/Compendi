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
        return f"\n<\nuser_id={self.id},\n email={self.email},\n username={self.username},\n hashed_pass={self.hashed_password},\n joined={self.created}\n>\n"
    
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
    name = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, default=datetime.now)
    
    ### FOREIGN KEYS
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    root_folder_id = db.Column(db.Integer, db.ForeignKey('folders.folder_id'), nullable=True)
        
    ### RELATIONSHIPS 
    user = db.relationship('Users', foreign_keys=[user_id])
    folders = db.relationship('Folders', back_populates='project', foreign_keys=[root_folder_id])

    def __repr__(self):
        return f"\n<\nproject_id={self.project_id},\n name={self.name},\n desc={self.desc},\n created={self.created}\n>\n"
    
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
        return root_folder
        
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
    project = db.relationship("Projects", foreign_keys=[project_id])
    files = db.relationship("Files", back_populates='parent_folder')

    def __repr__(self):
        return f"\n<\nfolder_id={self.folder_id},\n is_root={self.is_root},\n name={self.name},\n created={self.created}\n>\n"
    
    ################ is having files here correct??????
    def __init__(self, name, is_root, project_id, parent_folder_id=None):
        if is_root is True:
            self.name = 'root_folder'
        else:
            self.name = name
        
        self.is_root = is_root
        self.created = datetime.now()
        
        self.project_id = project_id
        self.parent_folder_id = parent_folder_id
        
    def add_file(self, name):
        new_file = Files(name, self.project_id, self.folder_id)
        db.session.add(new_file)
        db.session.commit()
        return new_file
        
    def add_folder(self, name):
        new_folder = Folders(name, is_root=False, project_id=self.project_id, parent_folder_id=self.folder_id)
        db.session.add(new_folder)
        db.session.commit()
        return new_folder
    
    def get_parent_folder(self):
        return Folders.query.filter_by(folder_id=self.parent_folder_id).first()  
    
    def get_children(self):
        print(f'\n{self.name} children:\n-----------------\n')
        files = Files.query.filter_by(parent_folder_id=self.folder_id).all()
        folders = Folders.query.filter_by(parent_folder_id=self.folder_id).all()
        return files, folders
        
class Files(db.Model):
    '''Files Table'''
    
    __tablename__ = "files"


    file_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)
    
    ### FOREIGN KEYS
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    parent_folder_id = db.Column(db.Integer, db.ForeignKey('folders.folder_id'), nullable=True)

    ### RELATIONSHIPS 
    parent_folder = db.relationship("Folders", back_populates='files')
    project = db.relationship("Projects", foreign_keys=[project_id])
    images = db.relationship("Images", back_populates='parent_file')

    def __repr__(self):
        return f"\n<\nfile_id={self.file_id},\n name={self.name}, created={self.created},\n project_id={self.project_id},\n parent_folder_id={self.parent_folder_id}\n>\n"
    
    def __init__(self, name, project_id, parent_folder_id=None):
        self.name = name
        self.created = datetime.now()
        self.project_id = project_id
        self.parent_folder_id = parent_folder_id
    
    def add_image(self, public_id):
        new_image = Images(public_id=public_id, file_id=self.file_id)
        db.session.add(new_image)
        db.session.commit()
        return new_image
    
    def add_section(self, header, sub_header, body):
        new_section = Sections(header=header, sub_header=sub_header, body=body, file_id=self.file_id)
        db.session.add(new_section)
        db.session.commit()
        return new_section
    
class Images(db.Model):
    '''Images Table'''
    
    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    image_path = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)

    ### FOREIGN KEYS
    file_id = db.Column(db.Integer, db.ForeignKey('files.file_id'), nullable=False)
    
    ### RELATIONSHIPS
    parent_file = db.relationship('Files', foreign_keys=[file_id])

    def __repr__(self):
        return f"\n<\nimage_id={self.image_id}, public_id={self.public_id},\n created={self.created},\n file_id={self.file_id}\n>\n"
    
    def __init__(self, file_id, public_id):
        self.image_path = f'https://res.cloudinary.com/dgnwphqcb/image/upload/v1674513671/{public_id}'
        self.created = datetime.now()
        self.file_id = file_id



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
    parent_file = db.relationship('Files', foreign_keys=[file_id])

    def __repr__(self):
        return f"\n<\n section_id= {self.section_id},\n header= {self.header},\n sub_header= {self.sub_header},\n body= {self.body}\n created= {self.created},\n last_updated={self.last_updated}\n>\n"
    
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