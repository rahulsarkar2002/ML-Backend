from flask import Flask, request, jsonify
import util
import tensorflow as tf
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ✅ Load the model when the app starts (not only in __main__)
util.load_saved_artifacts()

@app.route('/')
def index():
    return {"message": "Backend is running!"}

@app.route('/predict', methods=['POST'])
def predict_digit():
    image_file = request.files['image']
    filename = secure_filename(image_file.filename)
    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (32, 32), interpolation=cv2.INTER_AREA)
    gaussian_3 = cv2.GaussianBlur(img, (9, 9), 10.0)
    img = cv2.addWeighted(img, 1.5, gaussian_3, -0.5, 0, img)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img = cv2.filter2D(img, -1, kernel)
    ret, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    image_array = img / 255
    image_array = tf.reshape(image_array, (1, 32, 32, 1))

    response = jsonify(str(int(util.get_prediction(image_array))))
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Handwritten Digit Prediction...")
    util.load_saved_artifacts()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

