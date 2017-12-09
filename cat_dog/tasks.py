from __future__ import absolute_import
import os
import io
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
from celery import shared_task
import pdb
# pdb.set_trace()
# from django.contrib.auth.models import CatDog


from celery import Celery
import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cat_dog.settings')
from django.conf import settings


app = Celery('cat_dog', backend='amqp', broker='pyamqp://')

# app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


