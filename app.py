import flask
import json
from PIL import Image
from io import BytesIO
import numpy
import collections
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from ml_utils import MlModel, correct_yolo_boxes, do_nms
import server_utils as utils

app = flask.Flask(__name__, static_url_path="", static_folder="static")
driver = None
driver = utils.SQL_driver()
driver.create_tables()


ml = MlModel()


@app.route("/")
def redirect_to_menu():
    return flask.redirect("menu.html")


@app.route("/api")
def redirect_to_apidoc():
    return flask.redirect("apidoc.html")


@app.route("/api/images")
def return_image_ids():
    return driver.select_images()


@app.route("/api/image/<int:img_id>")
def return_image(img_id):
    return driver.select_images(img_id=img_id)


@app.route("/api/images/label/<string:label>")
def return_images_by_label(label):
    label = label.lower()
    return driver.select_images(img_label=label)


@app.route("/api/images/labels")
def return_labels():
    return driver.select_labels()


@app.route("/api/images/delete/<int:img_id>", methods=['DELETE'])
def delete_image_by_id(img_id):
    return driver.delete_image(img_id=img_id)


@app.route("/api/save", methods=['POST'])
def save_image():
    data = flask.request.json
    bin_image = utils.base64_str_to_bytearray(data["image"])
    image = Image.open(BytesIO(bin_image))

    for rect in data["rects"]:
        label = rect["label"]
        if label != '':
            label = label.lower()
            left = int(rect["x"])
            bottom = int(rect["y"]) + int(rect["h"])
            right = int(rect["x"]) + int(rect["w"])
            top = int(rect["y"])
            labeled_image = image.crop((left, top, right, bottom))
            labeled_image = labeled_image.resize((32, 32))
            image_bytes = BytesIO()
            labeled_image.save(image_bytes, format='PNG')
            image_bytes = image_bytes.getvalue()
            driver.insert_image(image_bytes, label)
    return "Save image with its label in database\n" + json.dumps(data, indent=4)

@app.route("/api/recognize", methods=['POST'])
def recognize_image():
    data = flask.request.json
    bytearray_image = utils.base64_str_to_bytearray(data["image"])
    image = Image.open(BytesIO(bytearray_image))

    box = data["box"]
    left = int(box["x"])
    bottom = int(box["y"]) + int(box["h"])
    right = int(box["x"]) + int(box["w"])
    top = int(box["y"])
    image = image.crop((left, top, right, bottom))

    bytes_image = BytesIO()
    image.save(bytes_image, format='PNG')

    label = ml.categorize_object(bytes_image)
    output = {
        "label": label
    }
    print(output)
    return json.dumps(output, indent=4)

@app.route('/api/yolo', methods=['POST'])
def get_yolo():
    # return ml.get_yolo_prediction("ss")
    data = flask.request.json
    bytearray_image = utils.base64_str_to_bytearray(data["image"])
    base_image = Image.open(BytesIO(bytearray_image))

    # input_image = Image.open(open("frog_big.jpg", 'rb'))
    image_w, image_h = base_image.size
    input_image = base_image.resize((416, 416))
    image = img_to_array(input_image)
    image = image.astype('float32')
    image /= 255.0

    image = numpy.expand_dims(image, 0)
    class_threshold = 0.6
    yhat = ml.yolo.predict(image)
    # print([a.shape for a in yhat])

    anchors = [[116, 90, 156, 198, 373, 326], [30, 61, 62, 45, 59, 119], [10, 13, 16, 30, 33, 23]]
    boxes = list()
    for i in range(len(yhat)):
        boxes += ml.decode_netout(yhat[i][0], anchors[i], class_threshold, 416, 416)

    correct_yolo_boxes(boxes, image_h, image_w, 416, 416)
    do_nms(boxes, 0.5)
    v_boxes, v_labels, v_scores = ml.get_boxes(boxes, class_threshold)

    objects_list = []
    for i in range(len(v_boxes)):
        print(v_labels[i], v_scores[i], v_boxes[i])
        box = v_boxes[i]
        label = v_labels[i].lower()
        accurancy = v_scores[i]

        image = base_image.crop((box.xmin, box.ymin, box.xmax, box.ymax))
        image = image.resize((32, 32))
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()
        driver.insert_dataset(image_bytes, label, accurancy)

        element = collections.OrderedDict()
        element['label'] = label
        element['accurancy'] = accurancy
        element['left'] = box.xmin
        element['right'] = box.xmax
        element['top'] = box.ymin
        element['bottom'] = box.ymax
        objects_list.append(element)
        # print(element)

    return json.dumps(objects_list, indent=4)


@app.route('/api/yolo/get')
def get_yolo_dataset():
    return driver.select_dataset()

@app.route('/api/yolo/get/label/<string:label>')
def get_yolo_dataset_by_label(label):
    label = label.lower()
    return driver.select_dataset(img_label=label)

@app.route('/api/yolo/get/id/<int:img_id>')
def get_yolo_dataset_by_id(img_id):
    return driver.select_dataset(img_id=img_id)

@app.route("/api/yolo/get/labels")
def get_yolo_dataset_labels():
    return driver.select_dataset_labels()

@app.route("/api/yolo/delete/<int:img_id>", methods=['DELETE'])
def delete_dataset_by_id(img_id):
    return driver.delete_yolo_image(img_id=img_id)

app.run(debug=True, threaded=False)
