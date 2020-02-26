from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy.types import Integer, String, DateTime
from hashlib import md5

from . import dba

class MapType(dba.Model):
    __tablename__ = 'kartta_type'
    id = dba.Column(dba.Integer, primary_key = True)
    name = dba.Column(dba.String(50))

class MapTown(dba.Model):
    __tablename__ = 'kartta_paikkakunta'
    id = dba.Column(dba.Integer, primary_key = True)
    paikkakunta = dba.Column(dba.String(40))
    maa_id = dba.Column(dba.String(10))
    lat = dba.Column(dba.String(50))
    lon = dba.Column(dba.String(50))

class MapCountry(dba.Model):
    __tablename__ = 'kartta_maa'
    id = dba.Column(dba.Integer, primary_key = True)
    maa = dba.Column(dba.String(100))
    lat = dba.Column(dba.String(50))
    lon = dba.Column(dba.String(50))
    koodi = dba.Column(dba.String(2))

class MapSpot(dba.Model):
    __tablename__ = 'kartta_tieto'
    kartta_id = dba.Column(dba.Integer, primary_key = True)
    paikkakunta_id = dba.Column(dba.Integer)
    user_id = dba.Column(dba.Integer)
    nimi = dba.Column(dba.String(200))
    info = dba.Column(dba.String(255))
    tyyppi = dba.Column(dba.Integer)
    temp = dba.Column(dba.Integer)
    paivays = dba.Column(dba.DateTime, default=datetime.now)
    karttalinkki = dba.Column(dba.String(200))
    maa_id = dba.Column(dba.Integer)
    latlon = dba.Column(dba.String(200))

class LinkCategories(dba.Model):
    __tablename__ = 'link_categories'
    id = dba.Column(dba.Integer, primary_key = True)
    name = dba.Column(dba.String(255))
    user_id = dba.Column(dba.Integer)
    create_time = dba.Column(dba.DateTime, default=datetime.now)

class Links(dba.Model):
    __tablename__ = 'links'
    id = dba.Column(dba.Integer, primary_key = True)
    name = dba.Column(dba.String(255))
    url = dba.Column(dba.String(255))
    category = dba.Column(dba.Integer)
    user_id = dba.Column(dba.Integer)
    create_time = dba.Column(dba.DateTime, default=datetime.now, onupdate=datetime.now)

class PwdRecover(dba.Model):
    __tablename__ = 'pwdrecover'
    id = dba.Column(dba.Integer, primary_key = True)
    username = dba.Column(dba.String(50))
    email = dba.Column(dba.String(50))
    token = dba.Column(dba.String(50))
    create_time = dba.Column(dba.DateTime, default=datetime.now, onupdate=datetime.now)

class Uploads(dba.Model):
    __tablename__ = 'uploads'
    id = dba.Column(dba.Integer, primary_key = True)
    user_id = dba.Column(dba.String(50))
    create_time = dba.Column(dba.DateTime, default=datetime.now, onupdate=datetime.now)
    path = dba.Column(dba.String(50))

class Media(dba.Model):
    __tablename__ = 'media_table'
    media_id = dba.Column(dba.Integer, primary_key = True)
    media_topic = dba.Column(dba.String(50))
    media_desc = dba.Column(dba.String(50))
    media_text = dba.Column(dba.String(50))
    media_type = dba.Column(dba.String(50))
    media_genre = dba.Column(dba.String(50))
    story_type = dba.Column(dba.String(50))
    create_time = dba.Column(dba.String(50))
    owner = dba.Column(dba.String(50))
    lang_id = dba.Column(dba.Integer)
    country_id = dba.Column(dba.Integer)
    hidden = dba.Column(dba.Integer)

class Page(dba.Model):
    __tablename__ = 'general'
    id = dba.Column(dba.Integer, primary_key = True)
    page_id = dba.Column(dba.Integer)
    header = dba.Column(dba.String(50))
    text = dba.Column(dba.String(50))
    info = dba.Column(dba.String(50))
    lang_id = dba.Column(dba.Integer)

class User(dba.Model):
    __tablename__ = 'users'
    user_id = dba.Column(dba.Integer, primary_key = True)
    username = dba.Column(dba.String(50))
    password = dba.Column(dba.String(50))
    level = dba.Column(dba.String(50))
    name = dba.Column(dba.String(50))
    email = dba.Column(dba.String(50))
    location = dba.Column(dba.String(50))
    address = dba.Column(dba.String(50))
    postnumber = dba.Column(dba.String(50))
    bornyear = dba.Column(dba.String(50))
    email2 = dba.Column(dba.String(50))
    homepage = dba.Column(dba.String(50))
    info = dba.Column(dba.String(50))
    date = dba.Column(dba.String(50))
    hobbies = dba.Column(dba.String(50))
    extrainfo = dba.Column(dba.String(50))
    sukupuoli = dba.Column(dba.String(50))
    icq = dba.Column(dba.String(50))
    apulainen = dba.Column(dba.String(50))
    last_login = dba.Column(dba.DateTime, default=datetime.now, onupdate=datetime.now)
    chat = dba.Column(dba.String(50))
    oikeus = dba.Column(dba.String(50))
    lang_id = dba.Column(dba.String(50))
    login_count = dba.Column(dba.String(50))
    lastloginip = dba.Column(dba.String(50))
    lastloginclient = dba.Column(dba.String(50))
    emails = dba.Column(dba.String(50))
    puhelin = dba.Column(dba.String(50))
    kantaasiakasnro = dba.Column(dba.String(50))
    lamina_lisatieto = dba.Column(dba.String(50))
    blogs = dba.Column(dba.String(50))
    user_showid = dba.Column(dba.String(50))
    messenger = dba.Column(dba.String(50))
    myspace = dba.Column(dba.String(50))
    rss = dba.Column(dba.String(50))
    youtube = dba.Column(dba.String(50))
    ircgalleria = dba.Column(dba.String(50))
    last_profile_update = dba.Column(dba.String(50))
    avatar = dba.Column(dba.String(50))
    def gravatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    flickr_username = dba.Column(dba.String(50))

class Comment(dba.Model):
    __tablename__ = 'kommentti'
    id = dba.Column(dba.Integer, primary_key = True)
    user_id = dba.Column(dba.Integer)
    header = dba.Column(dba.String(50))
    comment = dba.Column(dba.String(50))
    timestamp = dba.Column(dba.String(50))
    media_id = dba.Column(dba.String(50))
    comment_user_id = dba.Column(dba.String(50))
    youtube_id = dba.Column(dba.String(50))
    tapahtuma_id = dba.Column(dba.String(50))
    diary_id = dba.Column(dba.String(50))

class Storytype(dba.Model):
    __tablename__ = 'storytype'
    id = dba.Column(dba.Integer, primary_key= True)
    type_id = dba.Column(dba.Integer, dba.ForeignKey('media_table.story_type'))
    type_name = dba.Column(String(50))

class Genre(dba.Model):
    __tablename__ = 'genre'
    id = dba.Column(dba.Integer, primary_key= True)
    type_id = dba.Column(dba.Integer, dba.ForeignKey('media_table.media_genre'))
    type_name = dba.Column(String(50))

class Mediatype(dba.Model):
    __tablename__ = 'mediatype'
    id = dba.Column(dba.Integer, primary_key= True)
    type_id = dba.Column(dba.Integer, dba.ForeignKey('media_table.media_type'))
    type_name = dba.Column(String(50))

class Country(dba.Model):
    __tablename__ = 'countries'
    id = dba.Column(dba.Integer, dba.ForeignKey('media_table.country_id'), primary_key= True)
    country_code = dba.Column(String(50))
    country_name = dba.Column(String(50))