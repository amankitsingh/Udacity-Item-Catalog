# Udacity-Item-catalog-Project
SportCategoriesMenu App for Item catalog project
This is a python module that creates a website and JSON API for a list of sport categories. Each categories displays their menus and also provides user authentication using Google.
Registered users will have ability to edit and delete their own items. This application uses Flask,SQL Alchemy, JQuery,CSS, Javascript, and OAuth2 to create Item catalog website.
This App follow all the necessary CRUD functionality.
```
Installation
1. virtualBox
2. Vagrant
3. python 2.7
```
Instructions to Run the project

Requirements for the Project
```
1. Flask==0.12.0
2. Jinja2==2.8.1
3. gunicorn==19.6.0
4. sqlalchemy==1.2.7
```
Setting up OAuth 2.0
1. You will need to signup for a google account and set up a client id and secret.
2. Visit http://console.developers.google.com for google setup.

Setting up the Environment

1. clone or download the repo into vagrant environment.
2. Type command vagrant up,vagrant ssh.
3. In VM, cd /vagrant/catalog
4. Run python database.py to create the database.
5. Run Python moredata.py to add the menu items
6. Run python 'app.py'
7. open your webbrowser and visit http://localhost:8000/
8. Now you are ready to add ,delete ,edit categories and there items.

References
http://discussions.udacity.com/
