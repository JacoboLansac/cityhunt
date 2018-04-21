from app.ImageAnnotator import ImageAnnotator
import os

imm = ImageAnnotator()

names = os.listdir(os.getcwd() + '/resources')
test_images = [os.getcwd() + '/resources/' + name for name in names]

for image in test_images:
    landmarks = imm.get_landmark(image)
    print('\n', image, landmarks)



