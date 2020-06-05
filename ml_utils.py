from numpy import expand_dims
import tensorflow
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array


class MlModel:

    def __init__(self):
        self.yolo = load_model('ml/model.h5')
        self.yolo._make_predict_function()

    def get_yolo_prediction(self, image1):
        image = load_img("zebra.jpg", (416, 416))
        image = img_to_array(image)
        image = image.astype('float32')
        image /= 255.0
        # add a dimension so that we have one sample
        image = expand_dims(image, 0)
        yhat = self.yolo.predict(image)
        return str(yhat)
