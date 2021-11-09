import os
import uuid
import secrets
import tempfile

from flask import Flask, flash, render_template, request, redirect
from flask_pymongo import PyMongo
from pymongo.collection import Collection

from .model import Car, Prediction
from .predict import predict_label_from_image
from .util import validate_file_extension

__version__ = '0.0.1'

upload_folder = tempfile.mkdtemp()

# Configure Flask & Flask-PyMongo:
app = Flask(__name__, static_url_path='', static_folder=upload_folder)
app.config['SECRET_KEY'] = secrets.token_hex()
app.config['UPLOAD_FOLDER'] = upload_folder
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
pymongo = PyMongo(app)

# Get a reference to the collection.
car: Collection = pymongo.db.car
prediction: Collection = pymongo.db.prediction


@app.route('/', methods=['GET'])
def index():
    return render_template('index.jinja')


@app.route('/', methods=['POST'])
def predict():
    # check if the post request has the file part
    if 'predict_image' not in request.files:
        flash('Prediction image required')
        return redirect(request.url)

    predict_image = request.files['predict_image']

    # if user does not select file, browser also submit a empty part without filename
    if predict_image.filename == '':
        flash('Prediction image required')
        return redirect(request.url)

    # check if the file is one of the allowed types/extensions
    if predict_image and validate_file_extension(predict_image.filename):
        try:
            fn = str(uuid.uuid4()) + '.' + \
                predict_image.filename.rsplit('.', 1)[1].lower()
            fp = os.path.join(app.config['UPLOAD_FOLDER'], fn)
            predict_image.save(fp)

            predict_label = predict_label_from_image(fp)
            p = Prediction(
                prediction=predict_label[0], accuracy=float(predict_label[1]))
            prediction.insert_one(p.to_bson())
            return render_template('index.jinja', prediction=p.prediction, accuracy=p.accuracy, fn=fn)
        except Exception as e:
            flash("Prediction failed")
            return redirect(request.url)
    else:
        flash('Invalid file type')
        return redirect(request.url)


@app.route('/detail/<name>', methods=['GET'])
def car_detail(name):
    if name == "accord":
        name = "HONDA ACCORD"
    elif name == "camry":
        name = "TOYOTA CAMRY"
    elif name == "alphard":
        name = "TOYOTA ALPHARD"
    elif name == "Altis":
        name = "TOYOTA ALTIS"
    elif name == "vios":
        name = "TOYOTA VIOS"
    elif name == "bt-50":
        name = "MAZDA BT-50"
    elif name == "mazda2":
        name = "MAZDA2"
    elif name == "cx-8":
        name = "MAZDA CX-8"
    elif name == "c-hr":
        name = "TOYOTA C-HR"
    elif name == "brio":
        name = "HONDA BRIO"

    c = car.find_one_or_404({"name": name})
    return Car(**c).to_json()
