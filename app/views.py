import flask
from flask import render_template
from app import app
from app.ImageAnnotator import MonumentIdentifier
from app.ImageAnnotator import EmotionRecognition
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

@app.route('/upload-static', methods=['GET', 'POST'])
def upload_static():
    if request.method == 'POST' and 'photo' in request.files:
        outputname = photos.save(request.files['photo'])
        filename = '../static/img/' + outputname

        imm = MonumentIdentifier()
        landmarks = imm.get_landmark(filename)
        print(landmarks)
        return flask.jsonify(landmarks)

    return render_template('upload_static.html')



@app.route('/upload-url', methods=['GET','POST'])
def upload_url():

    im_url = 'http://media1.s-nbcnews.com/i/streams/2014/August/140827/1D274906654926-today-guard-140827.jpg'
    EmotionRecognition.get_emotions()

    return render_template('upload_url.html')



@app.route('/map')
def map():
    return render_template('map.html',
                           title='Home')


#