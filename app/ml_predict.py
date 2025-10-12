"""
Plant Disease Prediction Module with OpenCV Enhancement
"""

import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os
import cv2

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

def enhance_image_opencv(image_path):
    """Enhance image using OpenCV for better prediction"""
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    # 1. Denoise - Remove noise
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    
    # 2. Enhance contrast using CLAHE
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    enhanced = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    
    # 3. Sharpen image
    kernel = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
    enhanced = cv2.filter2D(enhanced, -1, kernel)
    
    # 4. Auto white balance
    result = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    
    return result

def check_image_quality(image_path):
    """Check if image quality is good enough"""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return False, "Cannot read image"
    
    # Check blur using Laplacian variance
    laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
    if laplacian_var < 100:
        return False, "Image too blurry. Please take a clearer photo."
    
    # Check brightness
    brightness = np.mean(img)
    if brightness < 40:
        return False, "Image too dark. Please use better lighting."
    if brightness > 220:
        return False, "Image too bright. Reduce exposure."
    
    return True, "Good quality"

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
        # Check image quality
        is_good, quality_msg = check_image_quality(image_path)
        
        # Enhance image with OpenCV
        enhanced_img = enhance_image_opencv(image_path)
        if enhanced_img is None:
            return {'error': 'Failed to process image'}
        
        # Convert to PIL and preprocess
        enhanced_img = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(enhanced_img)
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
            'quality_check': quality_msg,
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
