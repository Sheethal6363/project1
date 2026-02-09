import os
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import io
import json

app = Flask(__name__)
model = None
class_mapping = None
loading_error = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.h5')
INDICES_PATH = os.path.join(BASE_DIR, 'class_indices.json')

def load_resources():
    global model, class_mapping, loading_error
    
    # Load Model
    if os.path.exists(MODEL_PATH):
        try:
            model = load_model(MODEL_PATH)
            print(f"Model loaded successfully from {MODEL_PATH}")
            loading_error = None
        except Exception as e:
            loading_error = f"Error loading model from {MODEL_PATH}: {str(e)}"
            print(loading_error)
    else:
        loading_error = f"Model file not found at {MODEL_PATH}. Please train the model first."
        print(loading_error)

    # Load mapping
    if os.path.exists(INDICES_PATH):
        try:
            with open(INDICES_PATH, 'r') as f:
                class_mapping = json.load(f)
                # Convert keys to integers (json keys are strings)
                class_mapping = {int(k): v for k, v in class_mapping.items()}
            print(f"Class mapping loaded: {class_mapping}")
        except Exception as e:
            print(f"Error loading class mapping: {e}")
    else:
        # Fallback if file doesn't exist yet
        print("Mapping file not found, using default alphabetical.")
        class_mapping = {0: 'Reject', 1: 'Ripe', 2: 'Unripe'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    global model, class_mapping, loading_error
    if model is None:
        load_resources()
        if model is None:
            return jsonify({'error': f'Model not loaded: {loading_error}'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Preprocess
        img = Image.open(file.stream).convert('RGB')
        img = img.resize((128, 128))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        # Predict
        predictions = model.predict(img_array)
        
        # Get the class with highest probability
        predicted_class_idx = np.argmax(predictions[0])
        
        if class_mapping and predicted_class_idx in class_mapping:
            predicted_class = class_mapping[predicted_class_idx]
        else:
            predicted_class = "Unknown"
            print(f"DEBUG: Predicted Index {predicted_class_idx} not found in mapping {class_mapping}")

        confidence = float(predictions[0][predicted_class_idx])

        # Format predictions for all classes
        all_preds = {}
        if class_mapping:
            for idx, name in class_mapping.items():
                if idx < len(predictions[0]):
                    all_preds[name] = float(predictions[0][idx])

        return jsonify({
            'class': predicted_class,
            'confidence': confidence,
            'predictions': all_preds
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    load_resources()
    app.run(host='0.0.0.0', port=7860)
