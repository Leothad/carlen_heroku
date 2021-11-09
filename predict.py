import os

from tensorflow import keras
from PIL import Image
from skimage import transform
import numpy as np

from constant import PREDICT_MODEL_PATH, PREDICT_MODEL_SIZE, PREDICT_MODEL_LIST

model = keras.models.load_model(
    os.path.join(os.path.dirname(__file__), PREDICT_MODEL_PATH)
)


def predict_label_from_image(fp):
    img = Image.open(fp)
    img = np.array(img).astype(np.float32) / 255.0
    img = transform.resize(img, (PREDICT_MODEL_SIZE, PREDICT_MODEL_SIZE, 3))
    img = np.expand_dims(img, axis=0)
    result = model.predict(img)
    return PREDICT_MODEL_LIST[np.argmax(result)], result[0][np.argmax(result)]
