import flask
import json
from PIL import Image
import io
import server_utils as utils

app = flask.Flask(__name__, static_url_path="", static_folder="static")
driver = None

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
    return driver.select_images(img_id = img_id)

@app.route("/api/images/label/<string:label>")
def return_images_by_label(label):
    return driver.select_images(img_label = label)

@app.route("/api/images/labels")
def return_labels():
    return driver.select_labels()



@app.route("/api/save", methods=['POST'])
def save_image():
    data = flask.request.json
    bin_image = utils.base64_str_to_bytearray(data["image"])
    image = Image.open(io.BytesIO(bin_image))
    # with open("data_sent_by_post.png", "wb") as f:
    #     f.write(bin_image)
    for rect in data["rects"]:
        label = rect["label"]
        left = int(rect["x"])
        bottom = int(rect["y"]) + int(rect["h"])
        right = int(rect["x"]) + int(rect["w"])
        top = int(rect["y"])
        labeled_image = image.crop((left, top, right, bottom))
        labeled_image = labeled_image.resize((32, 32))
        image_bytes = io.BytesIO()
        labeled_image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()
        driver.insert_image(image_bytes, label)
    return "Save image with its label in database\n" + json.dumps(data, indent=4)


@app.route("/api/recognize", methods=['POST'])
def recognize_image():
    data = flask.request.json
    bin_image = utils.base64_str_to_bytearray(data["image"])

    output = {
        "guesses": [
            {
                "label": "cat",
                "percentage": 63
            },
            {
                "label": "cucumber",
                "percentage": 23
            }
        ]
    }
    return json.dumps(output, indent=4)


if __name__ == "__main__":
    driver = utils.SQL_driver()
    driver.create_tables()
    app.run(debug=True)
