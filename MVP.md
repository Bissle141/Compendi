# Writer's Cabinet #
- [Writer's Cabinet](#writers-cabinet)
  - [To Do:](#to-do)
  - [project organization:](#project-organization)
  - [MVP](#mvp)
    - [Possible additions](#possible-additions)
  - [View functions](#view-functions)

<br>

## To Do:

- [x] create virtual enviornment
  - [x] install dependencies
  - [x] pip freeze to requierments.txt
- [ ] create datebase
  - [ ] create seed_database file
- [ ] establish known view functions

<br>

## project organization:

```
📦 Compendi
 ┣ 📂data
 ┃ ┣ 📜files.json
 ┃ ┣ 📜folders.json
 ┃ ┗ 📜projects.json
 ┣ 📂env...
 ┣ 📂static
 ┃ ┣ 📜reset.css
 ┃ ┗ 📜styles.css
 ┣ 📂templates
 ┃ ┣ 📜base.html
 ┃ ┣ 📜file_view.html
 ┃ ┣ 📜folder_view.html
 ┃ ┣ 📜homepage_logged_in.html
 ┃ ┣ 📜login.html
 ┃ ┣ 📜projects.html
 ┃ ┗ 📜register.html
 ┣ 📜.gitignore
 ┣ 📜config.sh
 ┣ 📜crud.py
 ┣ 📜model.py
 ┣ 📜requirements.txt
 ┣ 📜seed_database.py
 ┗ 📜server.py
 ```

<br>

## MVP


- Login system
- Create project
- Create folder within projects
  - create nested folders
- Create files
  - set file attributes in edit mode (title, subtitle)
  - and/delete sections from file in edit mode
  - add imgs to file in edit mode
  - make sections collapsable within edit mode
  - Update and view file sections
    - should be collapsable outside of edit mode
- Gallery within files with imgs added

<br>

### Possible additions
--- 

-future features: maybe sooner rather than later
- User goals/stats
  - weekly/daily word count
- project based to do list which user can add/delete/update/markoff the items off 

## View functions

*?? incdicates items that could be added in the future*

- *homepage()*
  - navbar
    - logo &rarr; *homepage()*
    - if not logged in
      - login btn &rarr; *login_logout()*
      - register btn &rarr; *register()*
    - if logged in
      - profile icon &rarr; *profile()*
      - projects tab &rarr; *all_projects()*
      - logout btn &rarr; *login_logout()* 
  
![homepage not logged in](./Figmas/Homepage%20(not%20logged%20in).png)
  - if not logged in
    - graphic
    - register promt &rarr; *register()*
  
![homepage logged in](./Figmas/Homepage%20(logged%20in).png)
![homepage, creating new project](./Figmas/Homepage%20(logged%20in)%20_%20create%20project.png)
  - if logged in
    - all projects section
      - with create btn to create project
    - user stats section (encompasses all projects)
      - avg daily word count
      - avg weekly word count
- *profile()*
  - User info
  - ?? change password
  - ?? delete user
  - ?? add profile picture
- *login_logout()*
  - if logged in:
    - will log user out and redirect to *home_page()* with flash msg
      - "Sucessfully logged out"
  - if not logged in:
    - login section 
      - redirect &rarr; *homepage()*
- *register()*
    - register section
      - redirect &rarr; *login_register()* when completed sucessfully

