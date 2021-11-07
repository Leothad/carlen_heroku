#import Flask
from PIL import Image
from flask import Flask, render_template, request, redirect
from flask import jsonify
from flask import Response 
from bson import json_util
from keras.models import load_model
from skimage import transform
import numpy as np
import json
import pymongo
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

client = pymongo.MongoClient("mongodb+srv://carlen:XmHyP5culdETPnwG@cluster0.abpqf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",ssl=True,ssl_cert_reqs='CERT_NONE')
db = client.test


mydb = client["carlen"]
mycar = mydb["car"]
myprediction = mydb["prediction"]

# for x in mycar.find({ "name": "HONDA ACCORD"}):
#   print(x)

# mydict = { "name": "John", "address": "Highway 37" }
# y = myprediction.insert_one(mydict)

# print(y)

# client = MongoClient('mongodb://carlen:carlen@localhost/Carlen?retryWrites=true&w=majority')
# carlen
# XmHyP5culdETPnwG

#create an instance of Flask
app = Flask(__name__)


model = load_model('models.h5')
# model._make_predict_function()
input_shape = 224
cars=['Accord', 'Alphard', 'Altis', 'BT-50', 'Brio', 'C-HR', 'CX-8', 'Mazda2', 'Other', 'Vios']

def predict_label(img_path):
   np_image = Image.open(img_path)
   np_image = np.array(np_image).astype('float32')/255
   np_image = transform.resize(np_image, (input_shape,input_shape, 3))
   np_image = np.expand_dims(np_image, axis=0)
   result = model.predict(np_image)
   return cars[np.argmax(result)],result[0][np.argmax(result)]

   


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
    predict_result = p[0]
    predict_accuracy = float(p[1])
    mydict = {"prediction": predict_result, "accuracy": predict_accuracy}
    myprediction.insert_one(mydict)

    return render_template("home.html", prediction = p[0], accuracy = p[1], img_path = img_path)
  else:
    return redirect("/", code=303)

@app.route("/predicts", methods = ['GET', 'POST'])
def predicts():
  if request.method == 'POST':
    img = request.files['my_image']

    img_path = "static/" + img.filename
    img.save(img_path)

    p = predict_label(img_path)

    p = predict_label(img_path)
    predict_result = p[0]
    predict_accuracy = float(p[1])
    mydict = {"prediction": predict_result, "accuracy": predict_accuracy}
    myprediction.insert_one(mydict)

    return jsonify({"prediction": p[0], "accuracy": p[1], "img_path": img_path})
  else:
    return redirect("/", code=303)

@app.route("/static/<img_path>", methods = ['GET'])
def imgae(img_path):
    return img_path

@app.route("/detail/<carName>", methods = ['GET', 'POST'])
def detail(carName):
  print(carName)
  if carName == "accord": 
    carName = "HONDA ACCORD"
  elif carName == "camry":
    carName = "TOYOTA CAMRY"
  elif carName == "alphard":
    carName = "TOYOTA ALPHARD"
  elif carName == "Altis":
    carName = "TOYOTA ALTIS"
  elif carName == "vios":
    carName = "TOYOTA VIOS"
  elif carName == "bt-50":
    carName = "MAZDA BT-50"
  elif carName == "mazda2":
    carName = "MAZDA2"
  elif carName == "cx-8":
    carName = "MAZDA CX-8"
  elif carName == "c-hr":
    carName = "TOYOTA C-HR"
  elif carName == "brio":
    carName = "HONDA BRIO"
  
  
  carDetail = mycar.find({ "name": carName})

  return Response(
    json_util.dumps({carDetail}),
    mimetype='application/json'
  )

# config = {
#   'host':'carlen.mysql.database.azure.com',
#   'user':'carlen_admin@carlen',
#   'password':'nebxov-8kyrXy-wemzan',
#   'database':'carlens',
#   'client_flags': [mysql.connector.ClientFlag.SSL],
#   'ssl_ca': './DigiCertGlobalRootG2.crt.pem'
# }

# try:
#    conn = mysql.connector.connect(**config)
#    print("Connection established")
# except mysql.connector.Error as err:
#   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#     print("Something is wrong with the user name or password")
#   elif err.errno == errorcode.ER_BAD_DB_ERROR:
#     print("Database does not exist")
#   else:
#     print(err)
# else:
#   cursor = conn.cursor()
