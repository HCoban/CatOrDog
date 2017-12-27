# CatOrDog

[live](https://cat-or-dog.herokuapp.com)

CatOrDog is a fun Django application which you can upload an image of a cat or dog. A convolutional neural network is used to predict the type of animal (only cat or dog).

## Convolutional Neural Network (CNN)

The CNN was developed using `keras` and trained locally on my laptop (Ubuntu 16.04). Full source code of the CNN can be found in [its own repository](https://github.com/HCoban/Classifier-CatOrDog).

## Making predictions

Currently, there is one data model in the app called `CatDog`. This model has two fields, `animal` and `path`. The `animal` field shows the animal type, cat or dog, whereas the `path` is the url for the image.

The last 5 images are being rendered in the root page using bootstrap carousel. New predictions can be made by clicking the relevant button. I am using the [cloudinary upload widget](https://cloudinary.com/documentation/upload_widget) for uplading images. Using the widget, images are uploaded to cloudinary and the image url is saved to the database to the `path` field of the newly created `CatDog` instance. After that, the show page is rendered.

A [Celery](http://www.celeryproject.org/) worker with [RabbitMQ](https://www.rabbitmq.com/) broker is being used to asynchronously predict the animal type. The worker file can be found at `cat_dog/celery.py`. On the initialization of the worker the classifier is loaded from a `h5` file. If you are interested in how the `h5` file was generated, please click [here](https://github.com/HCoban/Classifier-CatOrDog).

`predict` method in the task file uses [`keras.preprocessing.image`](https://keras.io/preprocessing/image/) to convert the uploaded image to an array to be used by the CNN. When the prediction is completed the animal type is saved to `animal` field.

At this point, the user would most likely be still in the show page. I am making a new request after one second to render the predicted animal type. The predict method should be completed much faster than one second, thus the prediction should be visible.