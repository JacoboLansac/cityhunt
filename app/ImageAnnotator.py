import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


class ImageAnnotator:
    def __init__(self, keypath=None):
        if keypath is None:
            cw = os.getcwd()
            keypath = cw + '/jsonkey/tourkhana-1022aa40cf92.json'

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = keypath
        self.client = vision.ImageAnnotatorClient()


    def get_landmark(self, image_url):

        # The name of the image file to annotate
        file_name = os.path.join(os.path.dirname(__file__), image_name)

        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        response = self.client.landmark_detection(image=image)
        landmarks = response.landmark_annotations
        return [landmark.description for landmark in landmarks]





if __name__ == '__main__':
    cw = os.getcwd()
    keypath = '../jsonkey/tourkhana-1022aa40cf92.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = keypath
    client = vision.ImageAnnotatorClient()

    response = client.annotate_image({
    'image': {'source': {'image_uri': 'gs://my-test-bucket/image.jpg'}},
    ...
    'features': [{'type': vision.enums.Feature.Type.FACE_DETECTION}],
    ...})
    # Performs label detection on the image file
    # response = client.label_detection(image=image)
    # labels = response.label_annotations
    # print('Labels:')
    # for label in labels:
    #     print(label.description)
