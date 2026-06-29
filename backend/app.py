from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CORS(app)

model = load_model('fabric_model.h5')

def predict_fabric_quality(image_path):
    img = Image.open(image_path).convert('RGB').resize((150, 150))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    prediction = model.predict(img_array)
    return "Normal" if prediction[0][0] < 0.5 else "Defective"
# predict_fabric_quality
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    result = predict_fabric_quality(file_path)
    return jsonify({"message": f"AI Analysis complete: {result}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)