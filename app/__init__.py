import os
from flask import Flask, request, flash, g, render_template, jsonify, session, redirect, url_for, escape
from flask_session import Session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user , logout_user , current_user , login_required, UserMixin
from flask_selfdoc import Autodoc
from flask_navigation import Navigation

from .config import DefaultConfig

# Define the WSGI application object
app = Flask(__name__, instance_relative_config=True)

# DefaultConfig
app.config.from_object(DefaultConfig)

# Instance specific configurations
#app.config.from_pyfile('config.py')

# Database connection
db = MySQL(app)

# Login
sess = Session()

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_youtube.controllers import mod_youtube as youtube_module
from app.mod_soundcloud.controllers import mod_soundcloud as soundcloud_module
from app.mod_facebook.controllers import mod_facebook as facebook_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(youtube_module)
app.register_blueprint(soundcloud_module)
app.register_blueprint(facebook_module)

# Flask-Selfdoc
auto = Autodoc(app)

# Flask-Navigation
nav = Navigation(app)

nav.Bar('top', [
    nav.Item('Home', 'home'),
    nav.Item('News', 'news'),
    nav.Item('Youtube', 'youtube.youtube_playlists'),
    #nav.Item('Podcast', 'soundcloud.soundcloud_playlists'),
    nav.Item('Facebook', 'facebook.facebook_info'),
    nav.Item('Photos', 'view_photos_by_genre', {'genre': 'skateboarding'}, items=[
        nav.Item('Skateboarding', 'view_photos_by_genre', {'genre': 'skateboarding'}),
        nav.Item('Snowboarding', 'view_photos_by_genre', {'genre': 'snowboarding'}),
        nav.Item('Nollagang', 'view_photos_by_genre', {'genre': 'nollagang'}),
        nav.Item('Snowskate', 'view_photos_by_genre', {'genre': 'snowskate'}),
    ]),
    nav.Item('Videos', 'view_videos_by_genre', {'genre': 'skateboarding'}, items=[
        nav.Item('Skateboarding', 'view_videos_by_genre', {'genre': 'skateboarding'}),
        nav.Item('Snowboarding', 'view_videos_by_genre', {'genre': 'snowboarding'}),
    ]),
    nav.Item('Stories', 'stories', items=[
        nav.Item('Interviews', 'interviews'),
        nav.Item('Reviews', 'reviews'),
        #nav.Item('General', 'general'),
        #nav.Item('Other', 'other'),
    ]),
    nav.Item('Guides', 'guides'),
    #nav.Item('About', 'about'),
])

from . import api, views

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

