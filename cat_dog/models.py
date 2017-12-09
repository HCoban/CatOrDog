from django.db import models

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