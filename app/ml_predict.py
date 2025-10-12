"""
Plant Disease Prediction Module
"""

import tensorflow as tf
import numpy as np
from PIL import Image, ImageEnhance
import json
import os

MODEL_PATH = 'app/ml_models/plant_disease_model.h5'
CLASSES_PATH = 'app/ml_models/classes.json'
IMG_SIZE = 224

# Load model and classes
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(CLASSES_PATH, 'r') as f:
        class_names = json.load(f)
    MODEL_LOADED = True
except:
    MODEL_LOADED = False
    model = None
    class_names = []

def enhance_image_pil(image_path):
    """Enhance image using PIL for better prediction"""
    try:
        img = Image.open(image_path)
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.3)
        return img
    except:
        return None

def predict_disease(image_path):
    """
    Predict plant disease from image with OpenCV enhancement
    
    Args:
        image_path: Path to image file
        
    Returns:
        dict: {
            'disease': str,
            'confidence': float,
            'plant': str,
            'recommendations': list,
            'quality_check': str
        }
    """
    if not MODEL_LOADED:
        return {'error': 'Model not loaded'}
    
    try:
        # Enhance image with PIL
        img = enhance_image_pil(image_path)
        if img is None:
            return {'error': 'Failed to process image'}
        
        # Preprocess
        img = img.resize((IMG_SIZE, IMG_SIZE))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Predict
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        # Parse disease name
        disease_full = class_names[predicted_class]
        parts = disease_full.split('___')
        plant = parts[0].replace('_', ' ')
        disease = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'
        
        # Get recommendations
        recommendations = get_recommendations(disease, plant)
        
        return {
            'disease': disease,
            'confidence': round(confidence * 100, 2),
            'plant': plant,
            'recommendations': recommendations,
            'enhanced': True,
            'all_predictions': [
                {
                    'disease': class_names[i].split('___')[1].replace('_', ' '),
                    'confidence': round(float(predictions[0][i]) * 100, 2)
                }
                for i in np.argsort(predictions[0])[-5:][::-1]
            ]
        }
    except Exception as e:
        return {'error': str(e)}

def get_recommendations(disease, plant):
    """Get treatment recommendations for disease"""
    
    recommendations_db = {
        'healthy': [
            '✅ Your plant is healthy!',
            '🌱 Continue regular watering and fertilization',
            '☀️ Ensure adequate sunlight',
            '🔍 Monitor regularly for any changes'
        ],
        'Early blight': [
            '🍂 Remove infected leaves immediately',
            '💧 Avoid overhead watering',
            '🧪 Apply copper-based fungicide',
            '🌾 Rotate crops next season'
        ],
        'Late blight': [
            '⚠️ Remove and destroy infected plants',
            '💊 Apply fungicide containing chlorothalonil',
            '💨 Improve air circulation',
            '🚫 Avoid working with wet plants'
        ],
        'Bacterial spot': [
            '🦠 Remove infected plant parts',
            '💧 Use drip irrigation instead of overhead',
            '🧪 Apply copper-based bactericide',
            '🌱 Plant resistant varieties next time'
        ],
        'Powdery mildew': [
            '🍃 Remove affected leaves',
            '💨 Improve air circulation',
            '🧪 Spray with neem oil or sulfur',
            '☀️ Ensure plants get morning sun'
        ],
        'Leaf Mold': [
            '🍂 Remove infected leaves',
            '💨 Increase ventilation',
            '💧 Reduce humidity',
            '🧪 Apply fungicide if severe'
        ]
    }
    
    # Find matching recommendations
    for key in recommendations_db:
        if key.lower() in disease.lower():
            return recommendations_db[key]
    
    # Default recommendations
    return [
        '🔍 Consult with agricultural expert',
        '📸 Take clear photos for diagnosis',
        '🌱 Isolate affected plants',
        '💧 Adjust watering schedule'
    ]
