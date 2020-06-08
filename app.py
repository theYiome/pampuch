import flask
import json
from PIL import Image
from io import BytesIO
import numpy
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img

import server_utils as utils

app = flask.Flask(__name__, static_url_path="", static_folder="static")
driver = None
driver = utils.SQL_driver()
driver.create_tables()


from ml_utils import MlModel, BoundBox
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


@app.route("/api/image/<string:img_id>")
def return_image(img_id):
    return driver.select_images(img_id=img_id)


@app.route("/api/images/label/<string:label>")
def return_images_by_label(label):
    label = label.lower()
    return driver.select_images(img_label=label)


@app.route("/api/images/labels")
def return_labels():
    return driver.select_labels()


@app.route("/api/images/delete/<string:img_id>")
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

@app.route('/api/yolo')#, methods=['POST'])
def get_yolo():
    # data = flask.request.json
    # bytearray_image = utils.base64_str_to_bytearray(data["image"])
    # image = Image.open(BytesIO(bytearray_image))
    # image = image.resize((416, 416))

    input_image = load_img("zebra.jpg", (416, 416))
    image = img_to_array(input_image)
    image = image.astype('float32')
    image /= 255.0
    # add a dimension so that we have one sample
    image = numpy.expand_dims(image, 0)

    yhat = ml.yolo.predict(image)
    print([a.shape for a in yhat])
    # for thing in yhat:
    #     driver.insert_dataset(thing)
    anchors = [[116, 90, 156, 198, 373, 326], [30, 61, 62, 45, 59, 119], [10, 13, 16, 30, 33, 23]]
    boxes = list()
    for i in range(len(yhat)):
        # decode the output of the network
        boxes += ml.decode_netout(yhat[i][0], anchors[i], 0.6, 416, 416)
    v_boxes, v_labels, v_scores = ml.get_boxes(boxes, 0.6)
    # summarize what we found
    for i in range(len(v_boxes)):
        print(v_labels[i], v_scores[i], v_boxes[i])
        box = v_boxes[i]
        # get coordinates
        y1, x1, y2, x2 = box.ymin*416, box.xmin*416, box.ymax*416, box.xmax*416
        # calculate width and height of the box
        label = v_labels[i]
        accurancy = v_scores[i]
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        if x2 < 0:
            x2 = 0
        if y2 < 0:
            y2 = 0

        if x1 > 416:
            x1 = 416
        if y1 > 416:
            y1 = 416
        if x2 > 416:
            x2 = 416
        if y2 > 416:
            y2 = 416
        image = input_image.crop((x1, y1, x2, y2))
        image = image.resize((32, 32))
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()
        driver.insert_dataset(image_bytes, label, accurancy)
    # print(v_boxes)
    return str(yhat)
    # return ml.get_yolo_prediction(image)

@app.route('/api/yolo/get')
def get_yolo_dataset():

    return driver.select_dataset()


app.run(debug=True, threaded=False)
