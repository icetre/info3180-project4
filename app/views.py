from app import app, db
from time import gmtime, mktime
import os
from InfoForms import *
import hashlib
from random import randint
from Models import *
from image_getter import image_dem
import requests
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from flask import render_template, request, url_for, redirect, jsonify, flash, session
db.create_all()


@app.route('/')
def root():
    return redirect(url_for('.login'))


@app.route("/login", methods=["POST", "GET"])
def login():
    login = LoginForm(csrf_enabled=False)
    user = Profile()
    if request.method == "POST":
        login.populate_obj(user)
        if login.validate_on_submit():
            if user.validate():
                session['username'] = user.info3180_username
                return redirect(url_for('.home'))
        flash("Incorrect username or password")

    return render_template('login.html', form=login, formname='login')


@app.route("/register", methods=["POST", "GET"])
def signup():
    user = Profile()
    register = RegisterForm(csrf_enabled=False)
    if request.method == "POST":
        register.populate_obj(user)
        if register.validate_on_submit():
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('.login'))
    return render_template('register.html', form=register, formname="register")


@app.route('/api/user/register', methods=['GET', 'POST'])
def register():
    user = Profile(request.form['name'], request.form[
        'password'], request.form['email'])
    if not Profile.query.filter_by(info3180_email=request.form['email']).first():
        json_user = JsonSerialize(user)
        hash_object = hashlib.md5(b'user.info3180_username')
        db.session.add(user)
        db.session.commit()
        json_user.update(
            {"id": Profile.query.filter_by(info3180_email=request.form["email"]).first().id})
        data = {"token": hash_object.hexdigest(), "expires": mktime(gmtime()),
                "user": json_user, "messsage": "success"}
        out = jsonify(error=None, data=data)
        return out
    else:
        return jsonify(error="user already exists")


@app.route('/api/user/login', methods=['POST'])
def apiLogin():
    user = Profile(request.form['name'], request.form[
        'password'], request.form['email'])
    json_user = JsonSerialize(user)
    if user.validate():
        session['username'] = request.form['name']
        json_user = JsonSerialize(user)
        hash_object = hashlib.md5(b'user.info3180_username')
        uid = Profile.query.filter_by(
            info3180_email=request.form["email"]).first().id
        json_user.update({"id": uid})
        data = {"token": hash_object.hexdigest(), "expires": mktime(gmtime()),
                "user": json_user, "messsage": "success"}
        return jsonify(error=None, data=data)
    else:
        return jsonify(error=1, data={}, messsage="Bad user name or password")


@app.route('/home')
def home():
    if session.has_key('username'):
        item = Item.query.filter_by(
            info3180_username=session['username']).all()
        return render_template('home.html', items=item)
    return redirect(url_for('.login'))


@app.route('/logout')
def logout():
    if session.has_key('username'):
        session.pop('username', None)
    return redirect(url_for('.login'))


@app.route('/api/user/<int:uid>/wishlist', methods=['POST'])
def apiWishlist(uid):
    try:
        username = Profile.query.get(uid).info3180_username
        url = request.form['url']
        title = request.form['title']
        description = request.form['description']
        thumbnail = request.form['thumbnail']
        item = Item(username, url, title, description, thumbnail)
        db.session.add(item)
        db.session.commit()
        itemlst = Item.query.filter_by(info3180_username=username).all()
        wishlist = [JsonSerialize(i) for i in itemlst]
        data = {'data': wishlist}
        return jsonify(error=None, data=data, messsage='Success')
    except:
        return jsonify(error='1', data={}, messsage='No such wishlist exists')


@app.route('/api/user/<int:uid>/wishlist')
def getlist(uid):
    try:
        username = Profile.query.get(uid).info3180_username
        itemlst = Item.query.filter_by(info3180_username=username).all()
        wishlist = [JsonSerialize(i) for i in itemlst]
        data = {'data': wishlist}
        return jsonify(error=None, data=data, messsage='Success')
    except:
        return jsonify(error='1', data={}, messsage='No such wishlist exists')


@app.route('/api/thumbnail/process')
def get_thumbnail_lis():
    try:
        url = request.args['url']
        urlst = image_dem(url)
        data = {'thumbnails': urlst}
        return jsonify(error=None, data=data, messsage='Success')
    except:
        return jsonify(error='1', data={}, messsage='Unable to extract thumbnails')


@app.route('/thumbnail_url', methods=['GET', 'POST'])
def thumbnail_url():
    if session.has_key('username'):
        form = UrlForm()
        if request.method == 'POST':
            url = request.form['info3180_url']
            session['images'] = image_dem(url)
            session['url'] = url
            return redirect(url_for('.thumblist'))
        return render_template('thumbnail_url.html', form=form, formname="thumblist")
    return redirect(url_for('.login'))


@app.route('/thumblist')
def thumblist():
    if session.has_key('username'):
        images = session['images']
        session.pop('images', None)
        return render_template('thumblist.html', images=images)
    return redirect(url_for('.login'))


@app.route('/addwish', methods=['GET', 'POST'])
def addwish():
    if session.has_key('username'):
        item = Item()
        addwish = ThumbnailForm(csrf_enabled=False)
        _url = session['url']
        img_url = request.args.get('url')
        if _url != None:
            addwish.info3180_url.data = _url
        if request.method == 'POST':
            addwish.populate_obj(item)
            if addwish.validate_on_submit():
                item.info3180_username = session['username']
                item.info3180_thumbnail = img_url
                try:
                    db.session.add(item)
                    db.session.commit()
                    session['added'] = True
                    return redirect(url_for('.home'))
                except:
                    session['notadded'] = True
                    return redirect(url_for('.home'))
        return render_template('addwish.html', form=addwish, formname='addtowishlist')
    return redirect(url_for('.login'))


def get_thumbnail(url):
    thumbnailurl = url_for(
        'static', filename='img/thumbnail' + str(randint(0, 1000)) + '.jpg')
    filepath = os.path.dirname(os.path.abspath(__file__)) + thumbnailurl
    f = open(filepath, 'wb')
    f.write(requests.get(url).content)
    f.close()
    return thumbnailurl


def JsonSerialize(object=None):
    atrlst = dir(object)
    cls_name = "info3180_"
    attr_list = [i for i in atrlst if cls_name in i]
    print attr_list
    json_attr_dic = {}
    for i in attr_list:
        exec("attr=object.%s" % i)
        print i
        json_attr_dic.update({i.replace(cls_name, ""): attr})
    return json_attr_dic


@app.route('/sendemail', methods=['GET', 'POST'])
def sendemail():
    contact = ContactForm(csrf_enabled=False)
    fromaddr = 'therox116@gmail.com'
    contact.url.data = request.args.get('url')
    if request.method == 'POST':
        toaddr = request.form['recepientAddr']
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = '<' + toaddr + '>'
        msg['Subject'] = request.form['Subject']
        body = request.form['url'] + '\n' + request.form['Body']
        msg.attach(MIMEText(body))
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login('therox116@gmail.com', 'owoodmbxqpdjfihs')
        server.sendmail(fromaddr, toaddr.split(','), text)
        server.quit()
        return redirect(url_for('.home'))
    return render_template('EmailForm.html', form=contact, formname='EmailForm')
