
import os
from tensorflow.keras.models import load_model

MODEL_PATH = 'model.h5'

if os.path.exists(MODEL_PATH):
    try:
        print(f"Attempting to load model from {MODEL_PATH}...")
        model = load_model(MODEL_PATH)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"Model file not found at {MODEL_PATH}")
