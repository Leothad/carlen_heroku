import os
import uuid
import secrets
import tempfile

from flask import Flask, request, abort, url_for
from flask_pymongo import PyMongo
from flask_swagger_ui import get_swaggerui_blueprint
from pymongo.collection import Collection
from bson.objectid import ObjectId
from werkzeug.exceptions import HTTPException

from model import Car, Prediction
from predict import predict_label_from_image
from error import Error
from util import validate_file_extension, build_response

# Configure Flask & Flask-PyMongo:
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['TEMP_DIR'] = tempfile.mkdtemp()
pymongo = PyMongo(app, ssl=True, ssl_cert_reqs='CERT_NONE')

# Get a reference to the collection.
car: Collection = pymongo.db.car
prediction: Collection = pymongo.db.prediction

# Swagger
SWAGGER_URL = '/docs'
API_URL = '/static/openapi.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
)

app.register_blueprint(swaggerui_blueprint)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return Error(e.description, code).to_json(), code


@app.route('/predict', methods=['GET'])
def predict_list():
    try:
        predicts = prediction.find()
    except Exception:
        abort(500, description='Failed to retrieve cars')
    return build_response(True, data=[{**Prediction(**p).dict(), 'fn': url_for('predict_image', fn=p.get('fn')), '_link': url_for('predict_detail', id=p.get('_id'))} for p in predicts])


@app.route('/predict', methods=['POST'])
def predict():
    # check if the post request has the file part
    if 'predict_image' not in request.files:
        abort(400, description='Prediction image required')

    predict_image = request.files['predict_image']

    # if user does not select file, browser also submit a empty part without filename
    if predict_image.filename == '':
        abort(400, description='Prediction image required')

    # check if the file is one of the allowed types/extensions
    if predict_image and validate_file_extension(predict_image.filename):
        fn = str(uuid.uuid4()) + '.' + \
            predict_image.filename.rsplit('.', 1)[1].lower()
        fp = os.path.join(app.config.get('TEMP_DIR'), fn)
        predict_image.save(fp)
        # predict the label
        try:
            try:
                predict_label = predict_label_from_image(fp)
            except Exception:
                abort(500, description='Failed to predict label')

            # save the prediction image to the database
            try:
                with open(fp, 'rb') as f:
                    pymongo.save_file(fn, f, base='prediction')
            except Exception:
                abort(500, description='Failed to save image')
        finally:
            os.remove(fp)

        # save the prediction label to the database
        p = Prediction(
            prediction=predict_label[0],
            accuracy=float(predict_label[1]),
            fn=fn
        )
        try:
            result = prediction.insert_one(p.to_bson())
            app.logger.info(
                f'Prediction inserted: id={result.inserted_id} prediction={p.prediction} accuracy={float(p.accuracy)}')
        except Exception:
            abort(500, description='Failed to save prediction')

        return build_response(True, data={'id': str(result.inserted_id), '_link': url_for('predict_detail', id=ObjectId(str(result.inserted_id)))})
    else:
        abort(400, description='Invalid file type')


@app.route('/predict/<ObjectId:id>', methods=['GET'])
def predict_detail(id):
    p = prediction.find_one_or_404({'_id': id})
    return build_response(True, data={**Prediction(**p).dict(), 'fn': url_for('predict_image', fn=p.get('fn'))})


@app.route('/predict/images/<path:fn>')
def predict_image(fn):
    return pymongo.send_file(fn, base='prediction')


@ app.route('/cars', methods=['GET'])
def car_list():
    q = request.args.get('q')
    try:
        cars = car.find(
            {} if not q else Car().parse_raw(q).to_bson(),
            {'brand': 1, 'car': 1, 'model': 1, '_id': 1}
        )
    except Exception:
        abort(500, description='Failed to retrieve cars')
    return build_response(True, data=[{**Car(**c).dict(), '_link': url_for('car_detail', id=c.get('_id'))} for c in cars])


@app.route('/cars/<ObjectId:id>', methods=['GET'])
def car_detail(id):
    c = car.find_one_or_404({'_id': id})
    return build_response(True, data=Car(**c))
