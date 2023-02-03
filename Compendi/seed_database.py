import os

from random_username.generate import generate_username
from lorem_text import lorem
from model import db, Users, Projects, Folders, Files, Images, Sections, connect_to_db
import server


connect_to_db(server.app)

os.system('dropdb Compendi')
os.system('createdb Compendi')

db.create_all()

# Set num below to change how many users are generated!
number_of_users = 10
usernames = generate_username(number_of_users)

new_users = []
for i in range(number_of_users):
    new_users.append(Users(f'{usernames[i]}@email.com', usernames[i], 'password'))
new_users.append(Users('Bissle@email.com', 'Bissle', 'password'))
    
db.session.add_all(new_users)
db.session.commit()

new_projects = []
for user in new_users:
    for i in range(3):
        new_projects.append(Projects(name=f'project{i}', desc=lorem.paragraphs(1), user_id=user.id))

db.session.add_all(new_projects)
db.session.commit()

for project in new_projects:
    project.create_root()
    
root_folders = Folders.query.filter_by(is_root=True)
for folder in root_folders:
    child_folder = folder.add_folder(name='child_folder')
    child_folder.add_file(name='child_file')
    folder.add_file(name='root_child_file')
    
print('database seeded!')


##############################################################################

# model.db.session.add(model.Users('jon@gmail.com', 'jon_snow', 'urmyqueen'))
# model.db.session.add(model.Users('dany@gmail.com', 'dany', 'gocrazy'))

# model.db.session.commit()

# project = model.Projects('projectName', 'desc', 1)

# model.db.session.add(project)
# model.db.session.commit()
