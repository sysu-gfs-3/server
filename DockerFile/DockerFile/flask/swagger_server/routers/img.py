# -*- coding: utf-8 -*-
from werkzeug.utils import secure_filename
import time
import os
import requests
import json
import uuid
import hashlib 
import random
import string
from PIL import Image
import flask
from flask import (
    Blueprint, flash, redirect, request, session, g, url_for,Response,
    Flask, render_template, jsonify, request, make_response, send_from_directory, abort
)
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import datetime
import base64
from io import StringIO
from flask import current_app

import swagger_server.config as config

basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['jpeg', 'png', 'gif']) 


 
bp = Blueprint('img_bp', __name__, url_prefix='/')

uploaded_photos = UploadSet('photos')

def save_file(f): 
    file_dir = os.path.join(basedir, current_app.config['UPLOAD_FOLDER'])
    content = StringIO(f.read()) 
    try: 
        mime = Image.open(content).format.lower() 
        if mime not in ALLOWED_EXTENSIONS: 
            raise IOError()
        else:
            new_filename =  str(uuid.uuid4()) + '.' + mime
            f.save(os.path.join(file_dir, new_filename))
    except IOError: 
        print("error")



def gen_code():
    code = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return code

@bp.route("/images", methods=['POST']) 
def upload_temp_image():
    if request.method == 'POST':
        # check if the post request has the photo part
        if 'photo' not in request.files:
            return jsonify({'code': -1, 'photoname': '', 'msg': 'No photo part'})
        photo = request.files['photo']
        # if user does not select photo, browser also submit a empty part without photoname
        if photo.filename == '':
            return jsonify({'code': -1, 'photoname': '', 'msg': 'No selected photo'})
        else:
            try:
                photo.filename = gen_code() + '.png'
                photoname = uploaded_photos.save(photo)
                return jsonify({'code': 0, 'photoname': photoname, 'msg': uploaded_photos.url(photoname)})
            except Exception as e:
                print(e)
                return jsonify({'code': -1, 'photoname': '', 'msg': 'Error occurred'})
    else:
        return jsonify({'code': -1, 'photoname': '', 'msg': 'Method not allowed'})

@bp.route("/_uploads/photos/<image_path>")
def show_image(image_path):
    '''
    利用图片url用于显示
    '''
    with open(config.UPLOADED_PHOTOS_DEST + image_path, 'rb') as f:
        image = f.read()
    pic_url = Response(image, mimetype="image/jpeg")
    return pic_url


@bp.route('/upload')
def upload_test():
    return render_template('up.html')
 
 
# 上传文件
@bp.route('/upload', methods=['POST'], strict_slashes=False)
def upload():
    file_dir = os.path.join(basedir, current_app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    
    content = StringIO(f.read()) 
    try: 
        mime = Image.open(content).format.lower() 
        if mime not in ALLOWED_EXTENSIONS: 
            raise IOError()
        else:
            new_filename =  str(uuid.uuid4()) + '.' + mime
            f.save(os.path.join(file_dir, new_filename))
            return jsonify({"success": 0, "msg": "上传成功", "filename": new_filename})
            # 需要添加到用户头像
    except IOError: 
        return jsonify({"error": 1001, "msg": "上传失败"})

@bp.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        file_dir = os.path.join(basedir, current_app.config['UPLOAD_FOLDER'])
        if os.path.isfile(os.path.join(file_dir, filename)):
            return send_from_directory(file_dir, filename, as_attachment=True)
        else:
            return jsonify({"error": 1001, "msg": "获取头像失败"})
    
# show photo
@bp.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    file_dir = os.path.join(basedir, current_app.config['UPLOAD_FOLDER'])
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        return jsonify({"error": 1001, "msg": "获取头像失败"})

"""
def save_file_database(f):
    content = StringIO(f.read())
    try:
        mime = Image.open(content).format.lower()
        if mime not in ALLOWED_EXTENSIONS:
            raise IOError()
    except IOError:
        flask.abort(400)
    sha1 = hashlib.sha1(content.getvalue()).hexdigest()
    c = dict(
        content=bson.binary.Binary(content.getvalue()),
        mime=mime,
        time=datetime.datetime.utcnow(),
        sha1=sha1,
    )
    try:
        db.files.save(c)
    except pymongo.errors.DuplicateKeyError:
        pass
    return sha1

def get_file_fromdatabase(sha1):
  try:
    f = db.files.find_one({'sha1': sha1})
    if f is None:
      raise bson.errors.InvalidId()
    if flask.request.headers.get('If-Modified-Since') == f['time'].ctime():
      return flask.Response(status=304)
    resp = flask.Response(f['content'], mimetype='image/' + f['mime'])
    resp.headers['Last-Modified'] = f['time'].ctime()
    return resp
  except bson.errors.InvalidId:
    flask.abort(404)
"""
