import os
from flask import (
  Flask,
  render_template,
  request, 
  flash, 
  session, 
  redirect, 
  url_for
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
from cloudinary.uploader import upload
import cloudinary
from model import (
  connect_to_db, 
  db, 
  Users, 
  Projects, 
  Folders, 
  Files, 
  Sections, 
  Images
  )
from crud import (
  get_file_by_id,
  get_image_by_id,
  get_folder_by_id,
  get_project_by_id,
  get_section_by_id,
  get_user_by_id,
  get_user_by_username
  )
from forms import (
  LoginForm, 
  RegisterForm, 
  ProjectCreationForm,
  FolderFileCreationForm
  )

# App & Secret Key config
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

# Login Manager config
login_manager = LoginManager()
login_manager.init_app(app)
set_login_view = 'homepage'


#  Cloudinary Config
cloudinary.config(
  cloud_name = os.environ['CLOUDNAME'],
  api_key = os.environ['CLOUDAPIKEY'],
  api_secret = os.environ['APISECRET'],
  secure = True
)

# Upload
# upload("https://upload.wikimedia.org/wikipedia/commons/a/ae/Olympic_flag.jpg", public_id="olympic_flag")

# Transform
# url, options = cloudinary_url("olympic_flag", width=100, height=150, crop="fill")


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
        login_user(user, remember=False)
        
        return redirect(url_for("projects", user_id=user.id))
      
  print(login_form.errors) 
  return render_template('login.html', login_form=login_form)

@app.route('/register', methods=['POST', 'GET'])
def register():
  return render_template('register.html')

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return render_template('login.html')


############ VIEW FUNCTIONS ############

@app.route('/')
def homepage():
  return render_template('homepage.html',)

@app.route('/<user_id>/projects')
@login_required
def projects(user_id):
  return render_template('projects.html')

if __name__ == "__main__":
  connect_to_db(app)
  app.run(debug=True)