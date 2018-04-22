import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json


def get_landmark(image_name):

    cw = os.getcwd()
    keypath = cw + '/jsonkey/tourkhana-1022aa40cf92.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = keypath
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(os.path.dirname(__file__), image_name)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    return [landmark.description for landmark in landmarks]
    # return landmarks


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
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    data = data.decode("utf-8")
    print("Data loaded")
    list_emotions = []
    Npeople = len(json.loads(data))

    for i in range(Npeople):
        data_json = json.loads(data)[i]
        list_emotions.append(data_json["faceAttributes"]["emotion"])

    return list_emotions







if __name__ == '__main__':
    cw = os.getcwd()
    keypath = '../jsonkey/tourkhana-1022aa40cf92.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = keypath
    client = vision.ImageAnnotatorClient()

    response = client.annotate_image({
    'image': {'source': {'image_uri': 'https://github.com/JacoboLansac/foo_images/blob/master/cityhunt/frederik.jpg'}},
    'features': [{'type': vision.enums.Feature.Type.LANDMARK_DETECTION}],
    })
    print(response)


    response = client.annotate_image({
    'image': {'source': {'image_uri': 'https://github.com/JacoboLansac/foo_images/blob/master/cityhunt/frederik.jpg?raw=true'}},
    'features': [{'type': vision.enums.Feature.Type.LANDMARK_DETECTION}],
    })
    print(response)

    response = client.annotate_image({
    'image': {'source': {'image_uri': 'https://raw.githubusercontent.com/JacoboLansac/foo_images/master/cityhunt/frederik.jpg'}},
    'features': [{'type': vision.enums.Feature.Type.LANDMARK_DETECTION}],
    })
    print(response)


    landmarks = response.landmark_annotations
    [landmark.description for landmark in landmarks]

