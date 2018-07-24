from flask import Flask, render_template
from flask import request, redirect, jsonify, url_for, flash

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database import User, Categories, Base, Items

# Import Login session
from flask import session as login_session
import random
import string

# imports for gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# import login decorator
from functools import wraps

app = Flask(__name__)

# Connecting to Database and createing database session
engine = create_engine('sqlite:///datamenu.db')
#engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

# create a state token to request forgery.
# store it in the session for later validation


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login')
def showlogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Gathers data from Google Sign In API and
    # places it inside a session variable.
    # validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(
           json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application-json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # upgrade the authorization code in credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
           json.dumps('Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application-json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode("utf-8"))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    # Access token within the app
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
           json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    response = make_response(json.dumps('Succesfully connected users', 200))

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists or if it doesn't make a new one
    print 'User email is'+str(login_session['email'])
    user_id = getUserID(login_session['email'])
    if user_id:
        print 'Existing user#'+str(user_id)+'matches this email'
    else:
        user_id = createUser(login_session)
        print 'New user_id#'+str(user_id)+'created'
    login_session['user_id'] = user_id
    print 'Login session is tied to :id#'+str(login_session['user_id'])

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:150px;- \
      webkit-border-radius:150px;-moz-border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# Helper Functions
def createUser(login_session):
    newUser = User(
        name=login_session['username'], email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).first()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).first()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session.
@app.route('/gdisconnect')
def gdisconnect():
    # only disconnect a connected User
    access_token = login_session.get('access_token')
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    df = 'https://'
    url = df+'accounts.google.com/o/oauth2/revoke?token=%s' % login_session
    ['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is'
    print result
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("you have succesfully been logout")
        return redirect(url_for('showcategories'))
    else:
        flash("you were not logged in")
        return redirect(url_for('showcategories'))


# JSON APIs to view Categorie Information
@app.route('/categories/<int:categories_id>/menu/JSON')
def restaurantMenuJSON(categories_id):
    categories = session.query(Categories).filter_by(id=categories_id).one()
    items = session.query(Items).filter_by(
        categories_id=categories_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/categories/<int:categories_id>/items/<int:items_id>/JSON')
def ItemsJSON(categories_id, items_id):
    Litems = session.query(Items).filter_by(id=items_id).one()
    return jsonify(Litems=Litems.serialize)


@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Categories).all()
    return jsonify(categories=[r.serialize for r in categories])


# Show all categories
@app.route('/')
@app.route('/categories/')
def showcategories():
    categories = session.query(Categories).order_by(asc(Categories.name))
    return render_template('categories.html', categories=categories)


# Create a new Categorie
@app.route('/categories/new/', methods=['GET', 'POST'])
def newcategories():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newcategories = Categories(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newcategories)
        flash('New Categorie %s Successfully Created' % newcategories.name)
        session.commit()
        return redirect(url_for('showcategories'))
    else:
        return render_template('newcategories.html')

# Edit a categories


@app.route('/categories/<int:categories_id>/edit/', methods=['GET', 'POST'])
def editcategories(categories_id):
    if 'username' not in login_session:
        return redirect('/login')
    editcategories = session.query(
        Categories).filter_by(id=categories_id).one()
    if editcategories.user_id != login_session['user_id']:
        flash("Opps,You are not Authorized Bye Bye!!")
        return redirect(url_for('showcategories'))
    if request.method == 'POST':
        if request.form['name']:
            editcategories.name = request.form['name']
            flash('Categories Successfully Edited %s' % editcategories.name)
            return redirect(url_for('showcategories'))
    else:
        return render_template(
            'editcategories.html', categories=editcategories)


# Delete a categories
@app.route('/categories/<int:categories_id>/delete/', methods=['GET', 'POST'])
def deleteCategories(categories_id):
    if 'username' not in login_session:
        return redirect('/login')
    categoriesToDelete = session.query(
        Categories).filter_by(id=categories_id).one()
    if categoriesToDelete.user_id != login_session['user_id']:
        flash("Opps,You are not Authorized Bye Bye!!")
        return redirect(url_for('showcategories'))

    if request.method == 'POST':
        session.delete(categoriesToDelete)
        flash('%s Successfully Deleted' % categoriesToDelete.name)
        session.commit()
        return redirect(url_for('showcategories', categories_id=categories_id))
    else:
        return render_template(
            'deletecategories.html', categories=categoriesToDelete)

# Show a categories menu


@app.route('/categories/<int:categories_id>/')
@app.route('/categories/<int:categories_id>/menu/')
def showMenu(categories_id):
    categories = session.query(Categories).filter_by(id=categories_id).one()
    items = session.query(Items).filter_by(
        categories_id=categories_id).all()
    return render_template('menu.html', items=items, categories=categories)


# Create a new menu item
@app.route(
    '/categories/<int:categories_id>/menu/new/',
    methods=['GET', 'POST'])
def newItems(categories_id):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Categories).filter_by(id=categories_id).one()
    if request.method == 'POST':
        newItem = Items(
            name=request.form['name'],
            description=request.form['description'],
            categories_id=categories_id,
            user_id=categories.user_id)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showMenu', categories_id=categories_id))
    else:
        return render_template('newitems.html', categories_id=categories_id)


# Edit a item
@app.route(
    '/categories/<int:categories_id>/menu/<int:menu_id>/edit',
    methods=['GET', 'POST'])
def editItems(categories_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Items).filter_by(id=menu_id).one()
    categories = session.query(Categories).filter_by(id=categories_id).one()
    if editedItem.user_id != login_session['user_id']:
        flash("Opps,You are not Authorized Bye Bye!!")
        return redirect(url_for('showcategories'))

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showMenu', categories_id=categories_id))
    else:
        return render_template(
            'edititems.html',
            categories_id=categories_id,
            menu_id=menu_id,
            item=editedItem)


# Delete a menu item
@app.route(
    '/categories/<int:categories_id>/menu/<int:menu_id>/delete',
    methods=['GET', 'POST'])
def deleteItems(categories_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Categories).filter_by(id=categories_id).one()
    itemToDelete = session.query(Items).filter_by(id=menu_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        flash("Opps,You are not Authorized Bye Bye!!")
        return redirect(url_for('showcategories'))

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showMenu', categories_id=categories_id))
    else:
        return render_template('deleteitems.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'secret'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
