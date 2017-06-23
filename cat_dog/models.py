from django.db import models
import numpy as np
import tensorflow as tf
sess = tf.Session()
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.models import model_from_json
from keras.preprocessing import image
from keras import backend as K
K.set_session(sess)
import urllib.request
import io

def loadModel():
    json_file = open('classifier/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("classifier/model.h5")
    loaded_model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    return loaded_model

classifier = loadModel()
GRAPH = tf.get_default_graph()

class CatDog(models.Model):
    animal = models.CharField(max_length=100)
    path = models.TextField()

    def predictAnimal(self):
        global GRAPH
        with GRAPH.as_default():
            with urllib.request.urlopen(self.path) as open_image:
                test_image_file = io.BytesIO(open_image.read())
                test_image = image.load_img(test_image_file, target_size = (64, 64))
                test_image = image.img_to_array(test_image)
                test_image = np.expand_dims(test_image, axis = 0)
                result = classifier.predict(test_image)
                if result[0][0] == 1:
                    prediction = 'dog'
                else:
                    prediction = 'cat'

                self.animal = prediction
