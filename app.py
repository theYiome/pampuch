import flask
import json
import server_utils as utils

app = flask.Flask(__name__, static_url_path="/")


@app.route("/")
def redirect_to_menu():
    return flask.redirect("menu.html")


@app.route("/api")
def redirect_to_apidoc():
    return flask.redirect("apidoc.html")


@app.route("/api/images")
def return_image_ids():
    return "Returning ids of images in database"


@app.route("/api/image/<string:img_id>")
def return_image(img_id):
    return "Returning image with id: {}".format(img_id)


@app.route("/api/save", methods=['POST'])
def save_image():
    data = flask.request.json
    bin_image = utils.base64_str_to_bytearray(data["image"])

    with open("data_sent_by_post.png", "wb") as f:
        f.write(bin_image)
    
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