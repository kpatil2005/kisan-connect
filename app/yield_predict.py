"""
Crop Yield Prediction Module
Uses trained ML model for yield estimation
"""
import numpy as np
import pickle
import os

# Model cache
_models = {'dtr': None, 'preprocesser': None}

def load_models():
    if _models['dtr'] is None:
        model_path = os.path.join(os.path.dirname(__file__), 'ml_models', 'dtr.pkl')
        preprocesser_path = os.path.join(os.path.dirname(__file__), 'ml_models', 'preprocesser.pkl')
        
        with open(model_path, 'rb') as f:
            _models['dtr'] = pickle.load(f)
        
        with open(preprocesser_path, 'rb') as f:
            _models['preprocesser'] = pickle.load(f)
    
    return _models['dtr'], _models['preprocesser']

def predict_yield(crop, state, rainfall, temperature, humidity, ph, nitrogen, phosphorus, potassium, area):
    """
    Predict crop yield using trained ML model
    
    Returns:
        dict: {
            'yield': float (quintals per hectare),
            'total_yield': float (total quintals),
            'recommendations': list
        }
    """
    dtr, preprocesser = load_models()
    
    # Map crop names to dataset format
    crop_mapping = {
        'Rice': 'Rice, paddy',
        'Wheat': 'Wheat',
        'Cotton': 'Cotton',
        'Sugarcane': 'Sugar cane',
        'Maize': 'Maize',
        'Soybean': 'Soybeans',
        'Potato': 'Potatoes',
        'Tomato': 'Tomatoes'
    }
    
    mapped_crop = crop_mapping.get(crop, crop)
    
    # Use 2020 as default year and calculate pesticides estimate
    year = 2020
    pesticides = (nitrogen + phosphorus + potassium) / 10
    
    # Prepare features: Year, rainfall, pesticides, temperature, Area (state), Item (crop)
    features = np.array([[year, rainfall, pesticides, temperature, state, mapped_crop]], dtype=object)
    
    # Transform and predict
    transformed_features = preprocesser.transform(features)
    predicted_yield_hg = dtr.predict(transformed_features)[0]
    
    # Convert from hg/ha to quintals/ha (1 quintal = 100 kg, 1 hg = 0.1 kg)
    yield_per_hectare = predicted_yield_hg / 10
    total_yield = yield_per_hectare * area
    
    # Generate recommendations
    recommendations = []
    
    if rainfall < 600:
        recommendations.append('💧 Low rainfall detected - ensure adequate irrigation')
    elif rainfall > 2000:
        recommendations.append('🌊 High rainfall - ensure proper drainage to prevent waterlogging')
    else:
        recommendations.append('✅ Rainfall levels are optimal for crop growth')
    
    if temperature < 15:
        recommendations.append('❄️ Low temperature - consider protective measures')
    elif temperature > 35:
        recommendations.append('🌡️ High temperature - ensure adequate water supply')
    else:
        recommendations.append('🌡️ Temperature is ideal for crop cultivation')
    
    if humidity < 40:
        recommendations.append('🌵 Low humidity - increase irrigation frequency')
    elif humidity > 80:
        recommendations.append('💨 High humidity - monitor for fungal diseases')
    else:
        recommendations.append('✅ Humidity levels are good')
    
    if ph < 5.5 or ph > 8.0:
        recommendations.append('🧪 Soil pH not optimal - consider soil amendment')
    else:
        recommendations.append('🌿 Soil pH is within acceptable range')
    
    total_nutrients = nitrogen + phosphorus + potassium
    if total_nutrients < 100:
        recommendations.append('🧪 Low nutrient levels - apply balanced fertilizers')
    elif total_nutrients > 300:
        recommendations.append('✅ Nutrient levels are good - maintain current fertilization')
    else:
        recommendations.append('📊 Moderate nutrient levels - consider supplemental fertilization')
    
    recommendations.append(f'📈 Expected total production: {round(total_yield, 2)} quintals')
    
    return {
        'yield': round(yield_per_hectare, 2),
        'total_yield': round(total_yield, 2),
        'recommendations': recommendations
    }
