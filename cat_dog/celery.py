from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

from celery.concurrency import asynpool
from celery.signals import worker_init, worker_process_init
asynpool.PROC_ALIVE_TIMEOUT = 100.0 
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
from six.moves import cPickle

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cat_dog.settings')
app = Celery('cat_dog')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

tf_model = None

@worker_process_init.connect()
def on_worker_init(**_):
  global tf_model
  # Create server with model
  save_file = open('classifier/model_using_keras_save.h5', 'rb')
  import keras
  tf_model = keras.models.load_model(save_file)
  save_file.close()

@app.task
def predict(id, path):
  from .models import CatDog
  import io
  import numpy as np
  
  from celery.utils.log import get_task_logger
  from keras.preprocessing import image
  import urllib.request

  with urllib.request.urlopen(path) as open_image:
    test_image_file = io.BytesIO(open_image.read())
    test_image = image.load_img(test_image_file, target_size = (64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = tf_model.predict(test_image)
    if result[0][0] == 1:
        prediction = 'dog'
    else:
        prediction = 'cat'

  cat_dog = CatDog.objects.get(id=id)
  cat_dog.animal = prediction
  cat_dog.save()
  print(prediction)
  return prediction