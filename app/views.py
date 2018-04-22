import flask
from flask import render_template
from app import app
from app.ImageAnnotator import get_emotions
from app.ImageAnnotator import get_landmark
import request
#===================================================================================
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import url_for
import pandas as pd



photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)


@app.route('/')
@app.route('/index')
def index():
    print("Rendering index...")
    parameters = {'face_request':False,
                  'monument_request':False}

    return render_template('index.html',
                           parameters=parameters,
                           title='Home')


@app.route('/monument-form')
def monument_form():
    return render_template('index.html',
                           name='monument_url')

@app.route('/face-form')
def face_form():
    return render_template('index.html',
                           name='face_url')


@app.route('/monument-results', methods=['POST'])
def monument_results():
    recibed_url = request.form['monument_url']
    print(recibed_url)

    monument_results = get_landmark(image_url=recibed_url)
    print(monument_results)

    return render_template('index.html',
                           title='Monument results',
                           imageurl=recibed_url,
                           monument_results=monument_results)


@app.route('/face-results', methods=['POST'])
def face_results():
    recibed_url = request.form['face_url']

    emotions_response = get_emotions(image_url=recibed_url)
    emotions = dict(emotions_response[0])
    series = pd.Series(emotions)
    series.sort_values(inplace=True, ascending=False)
    emotions_dict = series.to_dict()

    return render_template('index.html',
                           title='Face results',
                           imageurl=recibed_url,
                           face_results=emotions_dict)






#===================================================================================
#####################################################################################
# Old previous
#####################################################################################
#===================================================================================
# @app.route('/')
# @app.route('/index')
# def index():
#     user = {'nickname':'City-Hunter'}
#     return render_template('index.html',
#                            user=user,
#                            title='Home')
#
# @app.route('/upload-static', methods=['GET', 'POST'])
# def upload_static():
#     if request.method == 'POST' and 'photo' in request.files:
#         outputname = photos.save(request.files['photo'])
#         filename = '../static/img/' + outputname
#
#         landmarks = get_landmark(filename)
#         print(landmarks)
#         return flask.jsonify(landmarks)
#
#     return render_template('upload.html',
#                            action=url_for('upload_static'))
#
#
# # @app.route('/upload-url', methods=['GET','POST'])
# # def upload_url():
# #     im_url = 'http://media1.s-nbcnews.com/i/streams/2014/August/140827/1D274906654926-today-guard-140827.jpg'
# #     EmotionRecognition.get_emotions()
# #
# #     return render_template('upload.html',
# #                            action=url_for('upload_url'))
#
#
# @app.route('/form')
# def my_form():
#     return render_template('preform.html')
#
# @app.route('/form', methods=['POST'])
# def my_form_post():
#     recibed_url = request.form['text']
#
#     emotions_response = get_emotions(recibed_url)
#     emotions = dict(emotions_response[0])
#     series = pd.Series(emotions)
#     series.sort_values(inplace=True, ascending=False)
#     emotions_dict = series.to_dict()
#
#     # return emotions
#     return render_template('postform.html',
#                            title='Loaded image',
#                            imageurl=recibed_url,
#                            emotions=emotions_dict)
#
# @app.route('/map')
# def map():
#     return render_template('map.html',
#                            title='Home')







#