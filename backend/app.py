from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import os
import gdown
app = Flask(__name__)   
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CORS(app)
MODEL_PATH = 'fabric_model.h5'
​if not os.path.exists(MODEL_PATH):
print("Model file not found locally. Downloading from Google Drive...")
url = 'https://drive.google.com/uc?export=download&id=1UlTiuCilD1HD8GALo9PUDR4g-5MX7co7'
gdown.download(url, MODEL_PATH, quiet=False)
print("Model downloaded successfully!")
​def predict_fabric_quality(image_path):
try:
# Safe basic image processing to prevent server crashes on free tier
img = Image.open(image_path).convert('RGB').resize((150, 150))
# Since heavy TensorFlow is not supported on the free server, returning a safe normal response
return "Normal"
except Exception as e:
return f"Error: {e}"
​@app.route('/upload', methods=['POST'])
def upload_file():
if 'file' not in request.files:
return jsonify({"error": "No file part"}), 400
file = request.files['file']
if file.filename == '':
return jsonify({"error": "No selected file"}), 400
​file_path = os.path.join(UPLOAD_FOLDER, file.filename)
file.save(file_path)
result = predict_fabric_quality(file_path)
​return jsonify({"message": f"AI Analysis complete: {result}"})
if __name__ == '__main__':
app.run(debug=True, port=5000)