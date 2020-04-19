import flask

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


@app.route("/api/save")
def save_image():
    return "Save image with its label in database"