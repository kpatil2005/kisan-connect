"""
Soil Report Scanner using Tesseract OCR with improved accuracy
"""
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_soil_data_from_image(image_path):
    """Extract pH, N, P, K values from soil report image"""
    try:
        img = Image.open(image_path)
        
        # Enhance image for better OCR
        img = img.convert('L')  # Convert to grayscale
        img = ImageEnhance.Contrast(img).enhance(2)  # Increase contrast
        img = ImageEnhance.Sharpness(img).enhance(2)  # Sharpen
        
        # Extract text with multiple configs for better accuracy
        text = pytesseract.image_to_string(img, config='--psm 6')
        text += ' ' + pytesseract.image_to_string(img, config='--psm 4')
        
        ph = None
        nitrogen = None
        phosphorus = None
        potassium = None
        
        # Find ALL numbers in text
        all_numbers = re.findall(r'([0-9]+\.?[0-9]*)', text)
        
        # pH patterns - very flexible
        ph_patterns = [
            r'pH[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'pH\s*value[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'Soil[\s_]pH[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'(?:^|\s)pH[:\s\-_=]*([0-9]+\.?[0-9]*)'
        ]
        for pattern in ph_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                val = float(match)
                if 0 <= val <= 14:
                    ph = val
                    break
            if ph:
                break
        
        # Nitrogen patterns - find N, Nitrogen, N2
        n_patterns = [
            r'Nitrogen[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'(?:^|\s|\()N[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'Available[\s_]N[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'N[\s_]content[:\s\-_=]*([0-9]+\.?[0-9]*)'
        ]
        for pattern in n_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                nitrogen = float(matches[0])
                break
        
        # Phosphorus patterns - find P, Phosphorus, P2O5
        p_patterns = [
            r'Phosphorus[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'(?:^|\s|\()P[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'Available[\s_]P[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'P2O5[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'P[\s_]content[:\s\-_=]*([0-9]+\.?[0-9]*)'
        ]
        for pattern in p_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                phosphorus = float(matches[0])
                break
        
        # Potassium patterns - find K, Potassium, K2O
        k_patterns = [
            r'Potassium[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'(?:^|\s|\()K[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'Available[\s_]K[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'K2O[:\s\-_=]*([0-9]+\.?[0-9]*)',
            r'K[\s_]content[:\s\-_=]*([0-9]+\.?[0-9]*)'
        ]
        for pattern in k_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                potassium = float(matches[0])
                break
        
        if ph or nitrogen or phosphorus or potassium:
            return {
                'ph': ph,
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'success': True,
                'message': 'Values extracted successfully'
            }
        else:
            return {'success': False, 'message': 'No values found. Try clearer image.'}
            
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}
