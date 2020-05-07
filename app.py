import flask
import json
from PIL import Image
import io
import server_utils as utils

app = flask.Flask(__name__, static_url_path="", static_folder="static")


@app.route("/")
def redirect_to_menu():
    return flask.redirect("menu.html")


@app.route("/api")
def redirect_to_apidoc():
    return flask.redirect("apidoc.html")


@app.route("/api/images")
def return_image_ids():
    connection = utils.sql_connection()
    return utils.sql_get_images(connection)


@app.route("/api/image/<string:img_id>")
def return_image(img_id):
    connection = utils.sql_connection()
    return utils.sql_get_images(connection, img_id)


@app.route("/api/save", methods=['POST'])
def save_image():
    data = flask.request.json
    bin_image = utils.base64_str_to_bytearray(data["image"])
    image = Image.open(io.BytesIO(bin_image))
    # with open("data_sent_by_post.png", "wb") as f:
    #     f.write(bin_image)
    connection = utils.sql_connection()
    for rect in data["rects"]:
        label = rect["label"]
        left = int(rect["x"])
        bottom = int(rect["y"]) + int(rect["h"])
        right = int(rect["x"]) + int(rect["w"])
        top = int(rect["y"])
        labeled_image = image.crop((left, top, right, bottom))
        labeled_image = labeled_image.resize((32, 32))
        utils.sql_insert_image(connection, labeled_image, label)
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
    connection = utils.sql_connection()
    utils.sql_create_table(connection)
    app.run(debug=True)
