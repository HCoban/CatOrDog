from __future__ import absolute_import
from celery import Celery
from celery.concurrency import asynpool
from celery.signals import worker_init, worker_process_init
asynpool.PROC_ALIVE_TIMEOUT = 100.0 
import os
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
from six.moves import cPickle

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django.conf import settings

app = Celery('cat_dog', backend='amqp', broker='pyamqp://')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

tf_model = None

@worker_process_init.connect()
def on_worker_init(**_):
  global tf_model
  # Create server with model
  logger.info('model for worker: started init')
  import tensorflow as tf
  sess = tf.Session()
  from keras import backend as K
  # K.set_session(sess)
  # json_file = open('classifier/model.json', 'r')
  save_file = open('../classifier/model.save', 'rb')
  tf_model = cPickle.load(save_file)
  save_file.close()
  # from keras.models import model_from_json
  # loaded_model_json = json_file.read()
  # json_file.close()
  # loaded_model = model_from_json(loaded_model_json)
  # print(loaded_model)
  # print("before loading")
  # loaded_model.load_weights("classifier/model.h5")
  
  # print("loaded weighs")
  # loaded_model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
  # print("model compiled")
  # GRAPH = tf.get_default_graph()
  # tf_model = loaded_model
  # logger.info('model for worker: initialized')

@app.task
def predict(id, path):
  from .models import CatDog
  import io
  import numpy as np
  
  from celery.utils.log import get_task_logger
  # sess = tf.Session()
  from keras.preprocessing import image
  
  import urllib.request
  

  print("1111")
  with urllib.request.urlopen(path) as open_image:
    print('2222')
    test_image_file = io.BytesIO(open_image.read())
    test_image = image.load_img(test_image_file, target_size = (64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    print("here")
    result = tf_model.predict(test_image)
    print("predicted")
    if result[0][0] == 1:
        prediction = 'dog'
    else:
        prediction = 'cat'

  # cat_dog = CatDog.objects.get(id=id)
  # cat_dog.animal = prediction
  # cat_dog.save()
  print(prediction)
  return prediction