import flask
from flask import render_template
from app import app
from app.ImageAnnotator import get_emotions
from app.ImageAnnotator import get_landmark
import request

from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import url_for
import pandas as pd

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)


# challenges = {'challenge1':False,
#               'challenge2':False,
#               'challenge3':False,
#               'challenge4':False,
#               'challenge5':False,
#               'challenge6':False,
#               'challenge7':False,
#               'challenge8':False,
#               }

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():

    results = {}

    if 'monument' in request.form:
        print("request.form -- monument")
        results = get_landmark(request.form['monument'])
        print(results)

        words = ' '.join(results['landmarks']).lower().split(' ')

        if any(['opera' in word for word in words]) and any(['denmark' in word for word in words]):
            results['opera'] = True
            results['last_result'] = 'opera'
            print('Opera Success')

        if any(['little' in word for word in words]) and any(['mermaid' in word for word in words]):
            results['mermaid'] = True
            results['last_result'] = 'mermaid'
            print('Mermaid Success')

        if any(['frederik' in word for word in words]):
            results['frederik'] = True
            results['last_result'] = 'frederik'
            print('Frederik Success')

        return render_template('index.html',
                        results=results,
                        title='Home',
                        imageurl=request.form['monument'])

    elif 'face' in request.form:
        print("request.form -- face")
        results = get_emotions(request.form['face'])
        print(results)
        max_em = 'happiness'
        max_val = 0
        for em,val in results['emotions'].items():
            if val > max_val:
                max_em = em
                max_val = val
        if max_em == 'happiness':
            results['amalienborg'] = True
            results['last_result'] = 'amalienborg'

        return render_template('index.html',
                        results=results,
                        title='Home',
                        imageurl=request.form['face'])

    else:
        print("None request done yet")

    return render_template('index.html',
                           title='Home',
                           results=results,
                           titulito='Challenge 1',
                           content='Try to make the guards smile and take a picture of them!')



# def monument_results():




# @app.route('/monument-form')
# def monument_form():
#     return render_template('index.html',
#                            name='monument_url')
#
# @app.route('/face-form')
# def face_form():
#     return render_template('index.html',
#                            name='face_url')
#
#
# @app.route('/monument-results', methods=['POST'])
# def monument_results():
#     recibed_url = request.form['monument_url']
#     print(recibed_url)
#
#     monument_results = get_landmark(image_url=recibed_url)
#     print(monument_results)
#
#     return render_template('index.html',
#                            title='Monument results',
#                            imageurl=recibed_url,
#                            monument_results=monument_results)
#
#
# @app.route('/face-results', methods=['POST'])
# def face_results():
#     recibed_url = request.form['face_url']
#
#     emotions_response = get_emotions(image_url=recibed_url)
#     emotions = dict(emotions_response[0])
#     series = pd.Series(emotions)
#     series.sort_values(inplace=True, ascending=False)
#     emotions_dict = series.to_dict()
#
#     return render_template('index.html',
#                            title='Face results',
#                            imageurl=recibed_url,
#                            face_results=emotions_dict)
#
#
# @app.route('/form-face', methods=['POST'])
# def evaluate_face():
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
