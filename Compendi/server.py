import os
from flask import (
  Flask,
  render_template,
  request, 
  flash, 
  session, 
  redirect, 
  url_for,
  )
from flask_login import (
  LoginManager, 
  login_required, 
  login_user, 
  logout_user,
  current_user,
  set_login_view
  )
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload, destroy
import cloudinary
from model import (
  connect_to_db, 
  db, 
  Users, 
  )
from crud import (
  get_file_by_id,
  get_image_by_id,
  get_folder_by_id,
  get_project_by_id,
  get_section_by_id,
  get_user_by_id,
  get_user_by_username,
  get_user_projects,
  get_sections,
  get_images,
  check_public_id,
  delete_project_cascade,
  delete_image_from_table,
  delete_section,
  delete_file,
  delete_folder,
  delete_project_from_table
  )
from forms import (
  LoginForm, 
  RegisterForm, 
  ProjectCreationForm,
  FolderFileCreationForm,
  FileMainForm,
  FileImageForm,
  FileSectionForm
  )

# App & Secret Key config
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

# Login Manager config
login_manager = LoginManager()
login_manager.init_app(app)
set_login_view = 'login'
LoginManager.login_message = 'Please login first.'


#  Cloudinary Config
cloudinary.config(
  cloud_name = os.environ['CLOUDNAME'],
  api_key = os.environ['CLOUDAPIKEY'],
  api_secret = os.environ['APISECRET'],
  secure = True
)


############ LOGIN MANAGEMENT ############

@login_manager.user_loader
def load_user(user_id):
  return get_user_by_id(user_id)

@app.route('/login', methods=['POST', 'GET'])
def login():
  login_form = LoginForm()
  
  if login_form.validate_on_submit():
    user = get_user_by_username(login_form.username.data)
    print(user)
    
    if user:
      if user.check_password(login_form.password.data):
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=login_form.remember.data)
        flash('Logged in successfully.', 'message')
        
        return redirect(url_for("projects"))
    flash('Input invalid, please try again.', 'error')
      
  return render_template('login.html', login_form=login_form)

@app.route('/register', methods=['POST', 'GET'])
def register():
  form = RegisterForm()
  
  if form.validate_on_submit():
    if Users.query.filter_by(username=form.username.data).first() == None:
      if Users.query.filter_by(email=form.email.data).first() == None:
        new_user = Users(form.email.data, form.username.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("You've been registered! Please log in.", 'message')
        return redirect(url_for('login'))
      else: flash('Email already in use.', 'error')
    else: flash('Username already in use.', 'error') 
    
  return render_template('register.html', form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  flash('Logged out successfully.', 'message')
  return redirect(url_for('login'))


############ VIEW FUNCTIONS ############

@app.route('/')
def homepage():
  return render_template('homepage.html',)

@app.route('/projects', methods=['POST', 'GET'])
@login_required
def projects():
  add_project_form = ProjectCreationForm()
  
  if add_project_form.validate_on_submit():
    current_user.add_project(name=add_project_form.project_name.data, desc=add_project_form.desc.data)
  
  return render_template('projects.html', projects=get_user_projects(current_user.id), add_project_form=add_project_form)

@app.route('/folder-view/<folder_id>', methods=['POST', 'GET'])
@login_required
def folder_view(folder_id):
  child_creation_form = FolderFileCreationForm()
  
  open_folder = get_folder_by_id(folder_id)
  project = get_project_by_id(open_folder.project_id)
  children = open_folder.get_children()
  
  if child_creation_form.validate_on_submit():
    if child_creation_form.type_selection.data == 'folder':
      new_folder = open_folder.add_folder(name=child_creation_form.name.data)
      return redirect(url_for('folder_view', folder_id=new_folder.folder_id))

    else:
      new_file = open_folder.add_file(name=child_creation_form.name.data)
      return redirect(url_for('file_view', file_id=new_file.file_id))
    
  return render_template('folder_view.html', folder=open_folder, project=project, children=children, create_form=child_creation_form)

@app.route('/file-view/<file_id>', methods=['POST', 'GET'])
@login_required
def file_view(file_id):
  open_file = get_file_by_id(file_id)
  main_form = FileMainForm()
  image_form = FileImageForm()
  section_form = FileSectionForm()
  
  return render_template(
    'file_view.html', 
    open_file=open_file, 
    main_form=main_form, 
    image_form=image_form, 
    section_form=section_form,
    sections=get_sections(file_id),
    images=get_images(file_id)
    )
  

@app.route('/file-edit/<file_id>/add-section', methods=['POST', 'GET'])
@login_required
def add_section(file_id):
  if request.method == "POST":
    section_name = request.form.get('sectionName', default= 'Untitled')
    section_body = request.form.get("sectionBody", default='...')

    working_file = get_file_by_id(file_id)
    working_file.add_section(header=section_name, body=section_body.strip())
    
  
  return redirect(url_for("file_view", file_id=file_id))

@app.route('/<file_id>/section-edit/<section_id>', methods=['POST', 'GET'])
@login_required
def edit_section(file_id, section_id):
  new_section_header = request.form.get('newSectionHeader', default= 'Untitled')
  new_section_body = request.form.get("sectionBody", default='...')
  
  working_section = get_section_by_id(section_id)
  working_section.header = new_section_header
  working_section.body = new_section_body
  
  db.session.commit()
  return redirect(url_for('file_view', file_id=file_id))
  
  

@app.route('/file-view/<file_id>/add-image', methods=['POST', 'GET'])
@login_required
def add_image(file_id):
  form = FileImageForm()
  
  if form.validate_on_submit():
    try:
      working_file = get_file_by_id(file_id)
      image_name = form.image_name.data
      image_link = (form.image_link.data).strip()
      
      public_id = image_name.strip().replace(' ', '_')
      if check_public_id(public_id) == False:
        upload(form.image_link.data, public_id=public_id)
        url, options = cloudinary_url(public_id, background='#F5F2EA', width=1000, crop="pad")

        working_file.add_image(public_id, url)
        flash('Image added!', 'message')
      else: flash('File name already in use', 'error')
    except:
      flash('An error occured', 'error')
  return redirect(url_for('file_view', file_id=file_id))

### DELETE VIEW FUNCTIONS
  
@app.route('/<file_id>/delete-image/<image_id>', methods=['POST', 'GET'])
@login_required
def delete_image(image_id, file_id):
  image_to_delete = get_image_by_id(image_id)
  try:
    destroy(image_to_delete.public_id)
  except:
    pass
  delete_image_from_table(image_id=image_id)
    
  return redirect(url_for('file_view', file_id=file_id))

@app.route('/delete/<parent_folder_id>/<folder_id>', methods=['POST', 'GET'])
@login_required
def delete_folder(parent_folder_id, folder_id):
  try:
    folder_to_delete = get_folder_by_id(folder_id)
    db.session.delete(folder_to_delete)
    db.session.commit()
  except:
    flash('Error, folder was not deleted', 'error')
    
  return redirect(url_for('folder_view', folder_id=parent_folder_id))
  

@app.route('/delete/<project_id>', methods=['POST', 'GET'])
@login_required
def delete_project(project_id):
  project_to_delete = get_project_by_id(project_id)
  project_to_delete.root_folder_id = None
  db.session.commit()
  
  project = delete_project_cascade(project_id)
  try:
    for image in project['images']:
      destroy(image.public_id)
      db.session.delete(image)
      db.session.commit()
  except:
    print('image')
  
  try:  
    for section in project['sections']:
      db.session.delete(section)
      # delete_section(section.section_id)
      db.session.commit()
  except:
    print('section')
  
  try:  
    for files in project['files']:
      db.session.delete(files)
      # delete_file(files.file_id)
      db.session.commit()
  except:
    print('file')
  
  try:  
    for folder in project['folders']:
      db.session.delete(folder)
      # delete_folder(folder.folder_id)
      db.session.commit()
  except:
    print('folder')
      
  
  db.session.delete(project['root_folder'])
  db.session.commit()
  
  db.session.delete(project['project'])
  db.session.commit()

  return redirect(url_for('projects'))




if __name__ == "__main__":
  connect_to_db(app)
  app.run(debug=True)