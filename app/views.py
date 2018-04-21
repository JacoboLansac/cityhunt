import flask
from flask import render_template
from app import app
from app.ImageAnnotator import ImageAnnotator
import request
#===================================================================================
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES


photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname':'City-Hunter'}
    return render_template('index.html',
                           user=user,
                           title='Home')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])

        # imm = ImageAnnotator()
        # landmarks = imm.get_landmark(filename)
        # print(landmarks)

        return filename
    return render_template('upload.html')


@app.route('/map')
def map():
    return render_template('map.html',
                           title='Home')


#