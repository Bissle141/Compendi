from model import Users, Projects, Folders, Files, Sections, Images, db
from sqlalchemy import delete

# MODEL METHODS:
## Users
###### .projects
###### check_password(password)
## Projects
###### create_root()
## Folders
###### add_file(name, sub_name)
###### add_folder(name)
###### get_parent_folder()
###### get_children()
## Files
###### add_image(public_id)
###### add_section(header, body)

# GET BY {}
def get_user_by_id(id):
    return Users.query.filter_by(id=id).first()

def get_user_by_username(username):
    return Users.query.filter_by(username=username).first()

def get_project_by_id(id):
    return Projects.query.filter_by(project_id=id).first()

def get_folder_by_id(id):
    return Folders.query.filter_by(folder_id=id).first()

def get_file_by_id(id):
    return Files.query.filter_by(file_id=id).first()

def get_section_by_id(id):
    return Sections.query.filter_by(section_id=id).first()

def get_image_by_id(id):
    return Images.query.filter_by(image_id=id).first()

# Get folders children
def get_folder_children(folder_id):
    parent_folder = get_folder_by_id(folder_id)
    
    if Folders.query.filter_by(parent_folder_id=parent_folder.folder_id).first() == None:
        folders = None
    else: 
        folders = Folders.query.filter_by(parent_folder_id=parent_folder.folder_id).all()
    if Files.query.filter_by(parent_folder_id=parent_folder.folder_id).first() == None:
        files = None
    else: 
        files = Files.query.filter_by(parent_folder_id=parent_folder.folder_id).all()
    return [folders, files] 

# get projects by uder id ordered by created
def get_user_projects(user_id):
    if Projects.query.filter_by(user_id=user_id).first() != None:
        return Projects.query.filter_by(user_id=user_id).order_by(Projects.created)
    else: return None
    
# Get all sections for a given file
def get_sections(file_id):
    if Sections.query.filter_by(file_id=file_id).first() != None:
        return Sections.query.filter_by(file_id=file_id).order_by(Sections.created)
    else: return None
    
# get all images for file
def get_images(file_id):
    if Images.query.filter_by(file_id=file_id).first() != None:
        return Images.query.filter_by(file_id=file_id).order_by(Images.created)
    else: return None

# check if image id already exists, if true,pub_id is taken
def check_public_id(public_id):
    if Images.query.filter_by(public_id=public_id).first() == None:
        return False
    else: return True
    
# DELETE FUNCTIONS
def delete_image_from_table(image_id):
    try:
        Images.query.filter_by(image_id=image_id).delete()

        return True
    except:
        return False

def delete_section_from_table(id):
    Sections.query.filter_by(section_id=id).delete()

def delete_file_from_table(id):
    Sections.query.filter_by(file_id=id).delete()
    Images.query.filter_by(file_id=id).delete()
    Files.query.filter_by(file_id=id).delete()

def delete_folder_from_table(id):
    Folders.query.filter_by(folder_id=id).delete()

def delete_project_from_table(id):
    project = Projects.query.filter_by(project_id=id).first()
  


def delete_project_cascade(project_id):
    project = {
        'project': get_project_by_id(project_id),
        'root_folder': Folders.query.filter_by(project_id=project_id, is_root=True).first(),
        'folders': Folders.query.filter_by(project_id=project_id, is_root=False).all(),
        'files': Files.query.filter_by(project_id=project_id).all(),
        'images': Images.query.filter_by(project_id=project_id).all(),
        'sections': Sections.query.filter_by(project_id=project_id).all()
    }
    
    return project
        
   