import numpy
import tensorflow
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from PIL import Image
import server_utils as utils
from io import BytesIO
import matplotlib.pyplot as plt

def _sigmoid(x):
	return 1. / (1. + numpy.exp(-x))

class MlModel:

    def __init__(self):
        self.yolo = load_model('ml/model.h5')
        self.yolo._make_predict_function()
        self.yolo_categorization = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck",
                                    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
                                    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
                                    "giraffe",
                                    "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis",
                                    "snowboard",
                                    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
                                    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
                                    "banana",
                                    "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut",
                                    "cake",
                                    "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor",
                                    "laptop", "mouse",
                                    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
                                    "refrigerator",
                                    "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
        self.categorization = load_model('ml/object_categorization_model.h5', compile=False)
        self.categorization._make_predict_function()
        self.categorization_classification = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse',
                                              'ship', 'truck']

    def get_boxes(self, boxes, thresh):
        v_boxes, v_labels, v_scores = list(), list(), list()
        for box in boxes:
            for i in range(len(self.yolo_categorization)):
                if box.classes[i] > thresh:
                    v_boxes.append(box)
                    v_labels.append(self.yolo_categorization[i])
                    v_scores.append(box.classes[i] * 100)
        return v_boxes, v_labels, v_scores

    def decode_netout(self, netout, anchors, obj_thresh, net_h, net_w):
        grid_h, grid_w = netout.shape[:2]
        nb_box = 3
        netout = netout.reshape((grid_h, grid_w, nb_box, -1))
        nb_class = netout.shape[-1] - 5
        boxes = []
        netout[..., :2] = _sigmoid(netout[..., :2])
        netout[..., 4:] = _sigmoid(netout[..., 4:])
        netout[..., 5:] = netout[..., 4][..., numpy.newaxis] * netout[..., 5:]
        netout[..., 5:] *= netout[..., 5:] > obj_thresh

        for i in range(grid_h * grid_w):
            row = i / grid_w
            col = i % grid_w
            for b in range(nb_box):
                # 4th element is objectness score
                objectness = netout[int(row)][int(col)][b][4]
                if (objectness.all() <= obj_thresh): continue
                # first 4 elements are x, y, w, and h
                x, y, w, h = netout[int(row)][int(col)][b][:4]
                x = (col + x) / grid_w  # center position, unit: image width
                y = (row + y) / grid_h  # center position, unit: image height
                w = anchors[2 * b + 0] * numpy.exp(w) / net_w  # unit: image width
                h = anchors[2 * b + 1] * numpy.exp(h) / net_h  # unit: image height
                # last elements are class probabilities
                classes = netout[int(row)][col][b][5:]
                box = BoundBox(x - w / 2, y - h / 2, x + w / 2, y + h / 2, objectness, classes)
                boxes.append(box)
        return boxes

    def get_yolo_prediction(self, image):
        image = load_img("cat.jpg", (416, 416))
        image = img_to_array(image)
        image = image.astype('float32')
        image /= 255.0
        # add a dimension so that we have one sample	        # add a dimension so that we have one sample
        image = numpy.expand_dims(image, 0)
        yhat = self.yolo.predict(image)
        return str(yhat)

    def categorize_object(self, bytes_image):
        # image = plt.imread("frog.jpg")

        image = Image.open(bytes_image)
        image = numpy.array(image)

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
            print(self.categorization_classification[list_index[i]], ':', round(predictions[0][list_index[i]] * 100, 2),
                  '%')
        return self.categorization_classification[list_index[0]]


class BoundBox:
    def __init__(self, xmin, ymin, xmax, ymax, objness=None, classes=None):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.objness = objness
        self.classes = classes
        self.label = -1
        self.score = -1

    def get_label(self):
        if self.label == -1:
            self.label = numpy.argmax(self.classes)

        return self.label

    def get_score(self):
        if self.score == -1:
            self.score = self.classes[self.get_label()]

        return self.score

