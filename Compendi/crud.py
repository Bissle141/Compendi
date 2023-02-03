from model import Users, Projects, Folders, Files, Sections, Images

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
###### add_section(header, sub_header, body)

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


    
# DELETE Functions
def delete_project(project_id):
    '''will return dict with lists containing all to-be-deleted objs'''
    
    return {
    'project' : get_project_by_id(project_id),
    'folders' : Folders.query.filter_by(project_id=project_id).all(),
    'files' : Files.query.filter_by(project_id=project_id).all(),
    'images' : Images.query.filter_by(project_id=project_id).all(),
    'sections' : Sections.query.filter_by(project_id=project_id).all()
    }
    
    
    # <div id="galleryCarouselIndicators" class="carousel slide" data-ride="carousel">
    #                     <ol class="carousel-indicators">
    #                         <li data-target="#galleryCarouselIndicators" data-slide-to="0" class="active"></li>
                            
    #                         {% for i in range(0, (images|length)) %}
    #                         <li data-target="#galleryCarouselIndicators" data-slide-to="{{i+1}}"></li>
    #                         {% endfor %}
    
    #                     </ol>
                        
    #                     <!-- Images -->
    #                     <div class="carousel-inner">
    #                         <div class="carousel-item active">
    #                             <img class="d-block w-100" src="{{images[0].image_path}}" alt="Slide 1">
    #                         </div>
                            
    #                         {% for i in range(0, (images|length)) %}
    #                             <div class="carousel-item">
    #                                 <img class="d-block w-100" src="{{images[i+1].image_path}}" alt="Slide {{i+2}}">
    #                             </div>
    #                         {% endfor %}
    
    #                     </div>
    
    #                     <!-- left and right arrows -->
    #                     <a class="carousel-control-prev" href="#galleryCarouselIndicators" role="button" data-slide="prev">
    #                     <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    #                     <span class="sr-only">Previous</span>
    #                     </a>
    #                     <a class="carousel-control-next" href="#galleryCarouselIndicators" role="button" data-slide="next">
    #                     <span class="carousel-control-next-icon" aria-hidden="true"></span>
    #                     <span class="sr-only">Next</span>
    #                     </a>
    #                 </div>