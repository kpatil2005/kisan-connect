from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import google.generativeai as genai
from django.conf import settings

try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
except Exception as e:
    print(f"Gemini API configuration error: {e}")

@csrf_exempt
@require_http_methods(["POST"])
def ai_chatbot(request):
    """Standalone AI chatbot endpoint"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        user_language = data.get('language', 'en')
        
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)
        
        user_message_en = user_message
        
        if user_message_en.lower() in ['hello', 'hi', 'hey']:
            bot_response = "Hello! I'm your farming assistant. Ask me about crops, weather, fertilizers, or any agricultural questions!"
        else:
            prompt = f"You are a helpful farming assistant. Answer this question briefly: {user_message_en}"
            
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                if response and hasattr(response, 'text') and response.text:
                    bot_response = response.text.strip()
                else:
                    bot_response = "I'm here to help with farming questions. Could you please rephrase your question?"
            except Exception as api_error:
                bot_response = "I'm having trouble right now. Please ask about farming topics like crops or weather."
            
        return JsonResponse({'response': bot_response})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'response': 'I apologize, but I\'m having trouble right now. Please try asking about farming, crops, weather, or agricultural practices.'}, status=500)