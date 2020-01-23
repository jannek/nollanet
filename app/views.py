import os, uuid
import datetime
from flask import Flask, request, flash, g, render_template, jsonify, session, redirect, url_for, escape
import requests, json
from urllib.parse import urljoin # Python 3
from flask_paginate import Pagination, get_page_args
from werkzeug import secure_filename

from azure.storage import CloudStorageAccount
from azure.storage.blob import BlockBlobService, PublicAccess

from app.models import Media, Page, User, Comment, Storytype, Genre, Mediatype, Country

from . import app, dba, utils, auto

@app.route('/interviews')
def interviews():
    interviews = dba.session.query(Media.media_type.in_((4,5,))).join(Genre).join(Mediatype).join(Storytype).join(Country).add_columns(Media.media_id,
            (Genre.type_name).label("genre"),
            (Mediatype.type_name).label("mediatype_name"),
            (Storytype.type_name).label("storytype_name"),
            (Country.country_code).label("country_code"),
            Media.media_topic,
            Media.create_time,
            Media.owner).filter(Media.story_type==utils.get_story_type('interviews')).order_by(Media.create_time.desc())
    return render_template("views/interviews.html", interviews=interviews)

@app.route('/news')
def news():
    total = utils.get_total_news_count()
    page, per_page, offset = utils.get_page_args(page_parameter='page', per_page_parameter='per_page')
    news = dba.session.query(Media.media_type.in_((4,5,))).join(Genre).join(Mediatype).join(Storytype).join(Country).add_columns(Media.media_id,
            (Genre.type_name).label("genre"),
            (Mediatype.type_name).label("mediatype_name"),
            (Storytype.type_name).label("storytype_name"),
            (Country.country_code).label("country_code"),
            Media.media_topic,
            Media.create_time,
            Media.owner).filter(Media.story_type==utils.get_story_type('news')).order_by(Media.create_time.desc()).offset(offset).limit(per_page)
    pagination = utils.get_pagination(page=page, per_page=per_page, total=total, record_name=' news', format_total=True, format_number=True,)
    return render_template("views/news.html", news=news, pagination=pagination)

@app.route('/reviews')
def reviews():
    reviews = dba.session.query(Media.media_type.in_((4,5,))).join(Genre).join(Mediatype).join(Storytype).join(Country).add_columns(Media.media_id,
            (Genre.type_name).label("genre"),
            (Mediatype.type_name).label("mediatype_name"),
            (Storytype.type_name).label("storytype_name"),
            (Country.country_code).label("country_code"),
            Media.media_topic,
            Media.create_time,
            Media.owner).filter(Media.story_type==utils.get_story_type('reviews')).order_by(Media.create_time.desc())
    return render_template("views/reviews.html", reviews=reviews)

@app.route('/spotchecks')
def spotchecks():
    spotchecks = Media.query.filter_by(media_type=5).join(Genre).join(Mediatype).join(Storytype).join(Country).add_columns(Media.media_id,
            (Genre.type_name).label("genre"),
            (Mediatype.type_name).label("mediatype_name"),
            (Storytype.type_name).label("storytype_name"),
            (Country.country_code).label("country_code"),
            Media.media_topic,
            Media.create_time,
            Media.owner).filter(Media.story_type==utils.get_story_type('spotchecks')).order_by(Media.create_time.desc())

    return render_template("views/spotchecks.html", spotchecks=spotchecks)

@app.route('/')
def home():

    interviews = Media.query.filter(Media.media_type.in_((4,5,))).filter_by(story_type=utils.get_story_type('interviews')).order_by(Media.create_time.desc()).limit(10)
    news = Media.query.filter(Media.media_type.in_((4,5,))).filter_by(story_type=utils.get_story_type('news')).order_by(Media.create_time.desc()).limit(10)
    reviews = Media.query.filter(Media.media_type.in_((4,5,))).filter_by(story_type=utils.get_story_type('reviews')).order_by(Media.create_time.desc()).limit(10)
    spotchecks = Media.query.filter(Media.media_type.in_((4,5,))).filter_by(story_type=utils.get_story_type('spotchecks')).order_by(Media.create_time.desc()).limit(10)

    page, per_page, offset = utils.get_page_args(page_parameter='page', per_page_parameter='per_page')

    photos_skateboarding = Media.query.filter_by(media_type=1).filter_by(media_genre=utils.get_media_genre_id('skateboarding')).order_by(Media.create_time.desc()).limit(offset).limit(per_page)
    photos_snowboarding = Media.query.filter_by(media_type=1).filter_by(media_genre=utils.get_media_genre_id('snowboarding')).order_by(Media.create_time.desc()).limit(offset).limit(per_page)
    photos_nollagang = Media.query.filter_by(media_type=1).filter_by(media_genre=utils.get_media_genre_id('nollagang')).order_by(Media.create_time.desc()).limit(offset).limit(per_page)
    photos_snowskate = Media.query.filter_by(media_type=1).filter_by(media_genre=utils.get_media_genre_id('snowskate')).order_by(Media.create_time.desc()).limit(offset).limit(per_page)
    
    return render_template('index.html', 
        interviews=interviews, 
        news=news, 
        reviews=reviews,
        spotchecks=spotchecks,
        photos_skateboarding=photos_skateboarding,
        photos_snowboarding=photos_snowboarding,
        photos_nollagang=photos_nollagang,
        photos_snowskate=photos_snowskate)

@app.route('/guides')
def guides():
    guides = Page.query.filter_by(lang_id=2)
    return render_template("views/guides.html", guides=guides)

@app.route('/guide/<page_id>/')
def view_guide(page_id):
    guide = Page.query.filter_by(lang_id=2, page_id=page_id).first()
    return render_template('views/guide.html', guide=guide)

@app.route("/support")
def support():
    return render_template("views/support.html")

@app.route("/about")
def about():
    return render_template("views/about.html")

@app.route('/user/<username>/', methods=['GET'])
def view_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return render_template('views/user.html', user=user)

@app.route('/interview/<media_id>/')
def view_interviews_item(media_id):
    interview = Media.query.filter_by(media_id=media_id).first()
    return render_template('views/interview.html', interview=interview)

@app.route('/news/<media_id>/')
def view_news_item(media_id):
    news_item = Media.query.filter_by(media_id=media_id).first()
    return render_template('views/news_item.html', news_item=news_item)

@app.route('/review/<media_id>/')
def view_review_item(media_id):
    review = Media.query.filter_by(media_id=media_id).first()
    return render_template('views/review.html', review=review)

@app.route('/spotcheck/<media_id>/')
def view_spotcheck_item(media_id):
    spotcheck = Media.query.filter_by(media_id=media_id).first()
    return render_template('views/spotcheck.html', spotcheck=spotcheck)

@app.route('/youtube/')
def youtube():
    return redirect('playlists')

@app.route('/photos/')
def view_photos_default():
    return redirect('skateboarding')

@app.route('/photos/<string:genre>/')
def view_photos_by_genre(genre):
    media_genre = utils.get_media_genre_id(genre)
    total = utils.get_total_photos_count_by_genre(media_genre)
    page, per_page, offset = utils.get_page_args(page_parameter='page', per_page_parameter='per_page')
    photos = dba.session.query(Media).join(Country).add_columns(Media.media_id,
            (Country.country_code).label("country_code"),
            Media.media_topic,
            Media.create_time,
            Media.owner).filter(Media.media_type==1).filter(Media.media_genre==media_genre).order_by(Media.create_time.desc()).offset(offset).limit(per_page)
    pagination = utils.get_pagination(page=page, per_page=per_page, total=total, record_name=' photos', format_total=True, format_number=True,)                                 
    return render_template('views/photos.html', photos=photos, pagination=pagination)

@app.route('/videos/<string:genre>/')
def view_videos_by_genre(genre):
    media_genre = utils.get_media_genre_id(genre)
    total = utils.get_total_videos_count_by_genre(media_genre)
    page, per_page, offset = utils.get_page_args(page_parameter='page', per_page_parameter='per_page')
    videos = dba.session.query(Media).join(Country).add_columns(Media.media_id,
            (Country.country_code).label("country_code"),
            Media.media_topic,
            Media.create_time,
            Media.owner).filter(Media.media_type==6).filter(Media.media_genre==media_genre).order_by(Media.create_time.desc()).offset(offset).limit(per_page)
    pagination = utils.get_pagination(page=page, per_page=per_page, total=total, record_name=' videos', format_total=True, format_number=True)              
    return render_template('views/videos.html', videos=videos, pagination=pagination)

@app.route('/photo/<media_id>')
def view_photo(media_id):
    photo = dba.session.query(Media).join(Country).add_columns(Media.media_id,
        (Country.country_code).label("country_code"),
        Media.media_topic,
        Media.media_text,
        Media.create_time,
        Media.owner).filter(Media.media_id==media_id).first()
    comments = Comment.query.filter_by(media_id=media_id).filter(Comment.user_id == User.user_id).order_by(Comment.id.desc()).limit(100)
    return render_template('views/photo.html', photo=photo, comments=comments)

@app.route('/video/<string:media_id>')
def view_video(media_id):
    video = Media.query.filter_by(media_id=media_id).first()
    return render_template('views/video.html', video=video)

""" Admin """

@app.route("/logins/latest/")
def latest_logins():
    latest_logins = dba.session.query(User).order_by(User.last_login.desc()).limit(10)
    return render_template("views/admin/latest_logins.html", latest_logins=latest_logins)

@app.route("/media/latest/")
def media_latest():
    latest = dba.session.query(Media).join(Genre).join(Mediatype).join(Storytype).join(Country).add_columns(Media.media_id,
        (Genre.type_name).label("genre"),
        (Mediatype.type_name).label("mediatype_name"),
        (Storytype.type_name).label("storytype_name"),
        (Country.country_code).label("country_code"),
        Media.media_topic,
        Media.media_desc,
        Media.create_time,
        Media.owner).order_by(Media.create_time.desc()).limit(10)
    return render_template("views/admin/latest_media.html", latest=latest)

@app.route('/media/delete', methods = ['POST'])
def delete_media():
    if(session and session['logged_in'] and session['user_level'] == 1):
        if request.method == 'POST':
            media_id = request.form.get('media_id')
            Media.query.filter_by(media_id=media_id).delete()
            dba.session.commit()
            flash("Record " + media_id + " was deleted succesfully by " + session['username'] + ".")
    else:
        flash("Please login first")
    return redirect(url_for("home"))


""" User """

@app.route('/media/<path:filename>', methods=['GET'])
def media(filename):
    static_url = app.config.get('AZURE_BLOB_URI')
    if static_url:
        return redirect(urljoin(static_url, filename))
    return app.send_static_file(filename)

@app.route("/media/update/<media_id>", methods = ['POST', 'GET'])
def update_media(media_id):
    if request.method == 'POST':

        media = { 'media_id': request.form.get('media_id'),
                'media_genre': request.form.get('media_genre'),
                'media_type': request.form.get('media_type'),
                'story_type': request.form.get('story_type'),
                'media_topic': request.form.get('media_topic'),
                'media_text': request.form.get('media_text'),
                'media_desc': request.form.get('media_desc'),
                'country_id': request.form.get('country_id') }

        if(session and session['logged_in'] and session['user_level'] == 1):

            Media.query.filter_by(media_id=media_id).update(media)
            dba.session.commit()
            flash("Record " + media_id + " was updated by user " + session['username'])
            return redirect(url_for("home"))
        else:
            flash("Please login first")
            return redirect(url_for("home"))
    else:
        if(session and session['logged_in'] and session['user_level'] == 1):
            result = Media.query.filter_by(media_id=media_id).first()
            return render_template("views/user/update_media.html", result=result)
        else:
            flash("Please login first")
            return redirect(url_for("home"))

@app.route("/media/newpost", methods = ['POST', 'GET'])
def new_post():
    if(session and session['logged_in'] and session['user_level'] == 1):
        if request.method == 'POST':
            media = Media(media_type = request.form.get('media_type'), 
                        media_genre = request.form.get('media_genre'),
                        country_id = request.form.get('country_id'),
                        story_type = request.form.get('story_type'),
                        media_topic = request.form.get('media_topic'),
                        media_text = request.form.get('media_text'),
                        media_desc = request.form.get('media_desc'),
                        owner = session['username'],
                        create_time = utils.get_now(),
                        lang_id = 2)
            dba.session.add(media)
            dba.session.commit()

            flash("New post created with ID " + str(media.media_id))

            if(media.media_type == "1"):
                return redirect(url_for("view_photo", media_id=media.media_id)) 
            elif(media.media_type == "6"): 
                if(media.story_type == "0"):
                    return redirect(url_for("view_video", media_id=media.media_id))
            elif(media.media_type == "5"):
                if(media.story_type == "2"):
                    return redirect(url_for("view_reviews_item", review_id=media.media_id))
                elif(media.story_type == "3"):
                    return redirect(url_for("view_interviews_item", interview_id=media.media_id))
                elif(media.story_type == "4"):
                    return redirect(url_for("view_news_item", news_id=media.media_id))
            else:
                return redirect(url_for("home"))
        else:
            blobs = utils.get_my_blobs()
            return render_template("views/user/new_post.html", blobs=blobs)
    else:
        flash("Please login first")
        return redirect(url_for("home"))

@app.route("/my/posts/")
def my_posts():
    if(session and session['logged_in']):
        username = session['username']
        posts = dba.session.query(Media).join(Genre).join(Mediatype).join(Storytype).join(Country).add_columns(Media.media_id,
            (Genre.type_name).label("genre"),
            (Mediatype.type_name).label("mediatype_name"),
            (Storytype.type_name).label("storytype_name"),
            (Country.country_code).label("country_code"),
            Media.media_topic,
            Media.create_time,
            Media.owner).filter(Media.owner==username).order_by(Media.create_time.desc()).limit(10)
        return render_template("views/user/posts.html", posts=posts)
    else:
        flash("Please login first")
        return redirect(url_for("home"))

@app.route("/media/newupload", methods=['POST','GET'])
def new_upload():
    if request.method == 'POST':
        blob_service = utils.get_azure_blob_service()
        container = ''
        file_to_upload = request.files['file']
        filename = secure_filename(file_to_upload.filename)

        if(session and session['logged_in']):
            container = session['username']
            if not blob_service.exists(container):
                blob_service.create_container(container)
                blob_service.set_container_acl(container, public_access=PublicAccess.Blob)
        else:
            flash("Please login first")
            return redirect(url_for("home"))

        # Create Blob from stream
        try:
            blob_service.create_blob_from_stream(container, filename, file_to_upload)
            blob = app.config.get('AZURE_BLOB_URI')
            ref =  blob + '/' + container + '/' + filename
            flash("File " + ref + " was uploaded successfully")
        except:
            print("Something went wrong while uploading the files %s"%filename)
            flash("Something went wrong while uploading the files %s"%filename)
            pass

        return redirect(url_for("my_uploads"))
    return render_template("views/user/new_upload.html")

@app.route("/my/uploads/")
def my_uploads():
    blobs = utils.get_my_blobs()
    return render_template("views/user/uploads.html", blobs=blobs)

@app.route('/blob/delete', methods = ['POST'])
def delete_blob():
    blob_service = utils.get_azure_blob_service()
    if(session and session['logged_in']):
        container = session['username']
        if request.method == 'POST':
            blob_name = request.form.get('blob_name')
            blob_service.delete_blob(container, blob_name)
            flash("File " + blob_name + " was deleted successfully")
    else:
        flash("Please login first")
        return redirect(url_for("home"))
    return redirect(url_for("my_uploads"))