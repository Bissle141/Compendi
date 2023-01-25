import os
from datetime import datetime

import loremipsum
import crud
import model
import server


model.connect_to_db(server.app)

os.system('dropdb Compendi')
os.system('createdb Compendi')

model.db.create_all()

model.db.session.add(model.Users('jon@gmail.com', 'jon_snow', 'urmyqueen'))
model.db.session.add(model.Users('dany@gmail.com', 'dany', 'gocrazy'))

model.db.session.commit()

project = model.Projects('projectName', 'desc', 1)

model.db.session.add(project)
model.db.session.commit()

project.create_root()