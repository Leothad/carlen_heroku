#import Flask
from PIL import Image
from flask import Flask, render_template, request
from keras.models import load_model
from skimage import transform
import numpy as np
import sqlite3 as sql
import mysql.connector
from mysql.connector import errorcode

#create an instance of Flask
app = Flask(__name__)


model = load_model('models.h5')
# model._make_predict_function()
input_shape = 224
cars=['Alphard', 'Altis', 'BT-50', 'Brio', 'C-HR', 'CRV', 'CX-8', 'Mazda2', 'Other', 'Vios']

def predict_label(img_path):
   np_image = Image.open(img_path)
   np_image = np.array(np_image).astype('float32')/255
   np_image = transform.resize(np_image, (input_shape,input_shape, 3))
   np_image = np.expand_dims(np_image, axis=0)
   result = model.predict(np_image)
   return cars[np.argmax(result)],result[0][np.argmax(result)]*100


# routes    
@app.route('/')
def home():
    return render_template('home.html')

@app.route("/about")
def about_page():
	return "About You..!!!"

@app.route("/predict", methods = ['GET', 'POST'])
def predict():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)

	return render_template("home.html", prediction = p[0], accuracy = p[1], img_path = img_path)

@app.route("/static/<img_path>", methods = ['GET'])
def imgae(img_path):

    return img_path

config = {
  'host':'carlen.mysql.database.azure.com',
  'user':'carlen_admin@carlen',
  'password':'nebxov-8kyrXy-wemzan',
  'database':'carlens',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': '/var/wwww/html/DigiCertGlobalRootG2.crt.pem'
}

try:
   conn = mysql.connector.connect(**config)
   print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = conn.cursor()




if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port="4114")