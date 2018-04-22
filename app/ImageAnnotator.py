import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json


def get_landmark(image_url="", image_name=""):

    cw = os.getcwd()
    print(cw)
    if cw[-3:] == 'app':
        keypath = cw + '/../jsonkey/tourkhana-1022aa40cf92.json'
    else:
        keypath = cw + '/jsonkey/tourkhana-1022aa40cf92.json'

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = keypath
    client = vision.ImageAnnotatorClient()

    if image_url:
        response = client.annotate_image({
            'image': {'source': {
                'image_uri': image_url}},
            'features': [{'type': vision.enums.Feature.Type.LANDMARK_DETECTION}],
        })
        return {'landmarks':[item.description for item in response.landmark_annotations]}

    elif image_name:
        file_name = os.path.join(os.path.dirname(__file__), image_name)
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)
        response = client.landmark_detection(image=image)
        landmarks = response.landmark_annotations
        return {'landmarks':[landmark.description for landmark in landmarks]}



def get_emotions(image_url=""):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '7cef923318814299bf3efb87d7ba809a',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': 'false',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,emotion'
    })

    body = json.dumps({
        "url": image_url
    })

    try:
        conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        print( "Obtaining response...")

        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        dataread = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



    jsondata = dict(json.loads(str(dataread.decode('utf-8'))[1:-1]))
    # jsondata = json.loads(data.decode('utf-8')[1:-1])
    emotions = jsondata['faceAttributes']['emotion']


    # data = data.decode("utf-8")
    # print("Data loaded")
    # list_emotions = []
    # Npeople = len(json.loads(data))
    #
    # print(Npeople)
    # for i in range(Npeople):
    #     data_json = json.loads(data)[i]
    #     list_emotions.append(data_json["faceAttributes"]["emotion"])

    return {'emotions':emotions}








if __name__ == '__main__':

    image_url = 'http://bh-s2.azureedge.net/bh-uploads/2016/01/1098_01.jpg'
    results = get_emotions(image_url=image_url)

    print(results)
    max_em = 'happiness'
    max_val = 0
    for em, val in results['emotions'].items():
        if val > max_val:
            max_em = em
            max_val = val

    if max_em == 'happiness':
        success = False
    else:
        success = True





    image_url = 'https://raw.githubusercontent.com/JacoboLansac/foo_images/master/cityhunt/sirenita.jpg'
    results = get_landmark(image_url)
    words = ' '.join(results['landmarks']).lower().split(' ')
    if any(['little' in word for word in words]) and any(['mermaid' in word for word in words]):
        print('Success')


    image_url = 'https://raw.githubusercontent.com/JacoboLansac/foo_images/master/cityhunt/opera1.jpg'
    results = get_landmark(image_url)
    words = ' '.join(results['landmarks']).lower().split(' ')
    if any(['opera' in word for word in words]) and any(['denmark' in word for word in words]):
        print('Success')

    image_url = 'https://raw.githubusercontent.com/JacoboLansac/foo_images/master/cityhunt/frederik.jpg'
    results = get_landmark(image_url)
    words = ' '.join(results['landmarks']).lower().split(' ')
    if any(['frederik' in word for word in words]):
        print('Success')








    cw = os.getcwd()
    keypath = '../jsonkey/tourkhana-1022aa40cf92.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = keypath
    client = vision.ImageAnnotatorClient()

    response = client.annotate_image({
    'image': {'source': {'image_uri': 'https://raw.githubusercontent.com/JacoboLansac/foo_images/master/cityhunt/frederik.jpg'}},
    'features': [{'type': vision.enums.Feature.Type.LANDMARK_DETECTION}],
    })
    print(response)


    landmarks = response.landmark_annotations
    {'landmarks': [landmark.description for landmark in landmarks]}

