import numpy
import tensorflow
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import matplotlib.pyplot as plt


class MlModel:

    def __init__(self):
        self.yolo = load_model('ml/model.h5')
        self.yolo._make_predict_function()
        self.categorization = load_model('ml/object_categorization_model.h5', compile=False)
        self.categorization._make_predict_function()
        self.categorization_classification = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse',
                                              'ship', 'truck']

    def get_yolo_prediction(self, image1):
        image = load_img("zebra.jpg", (416, 416))
        image = img_to_array(image)
        image = image.astype('float32')
        image /= 255.0
        # add a dimension so that we have one sample
        image = numpy.expand_dimsexpand_dims(image, 0)
        yhat = self.yolo.predict(image)
        return str(yhat)

    def categorize_object(self, image):
        image = plt.imread("shih-tzu.jpg")
        from skimage.transform import resize
        image = resize(image, (32, 32, 3))
        predictions = self.categorization.predict(numpy.array([image]))
        print(predictions)
        list_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        x = predictions
        for i in range(10):
            for j in range(10):
                if x[0][list_index[i]] > x[0][list_index[j]]:
                    temp = list_index[i]
                    list_index[i] = list_index[j]
                    list_index[j] = temp
        for i in range(5):
            print(self.categorization_classification[list_index[i]], ':', round(predictions[0][list_index[i]] * 100, 2), '%')
        return self.categorization_classification[list_index[0]]