from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import google.generativeai as genai
from django.conf import settings

# Configure Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)

@csrf_exempt
@require_http_methods(["POST"])
def ai_chatbot(request):
    """Standalone AI chatbot endpoint"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        user_language = data.get('language', 'en')
        
        print(f"Received message: '{user_message}'")
        print(f"Language: {user_language}")
        
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)
        
        # For now, work with English only to test basic functionality
        user_message_en = user_message
        
        # Simple test response first
        if user_message_en.lower() in ['hello', 'hi', 'hey']:
            bot_response = "Hello! I'm your farming assistant. Ask me about crops, weather, fertilizers, or any agricultural questions!"
        else:
            # Create farming-focused prompt
            prompt = f"You are a helpful farming assistant. Answer this question briefly: {user_message_en}"
            
            # Use Gemini API with detailed error handling
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                if response and hasattr(response, 'text') and response.text:
                    bot_response = response.text.strip()
                else:
                    bot_response = "I'm here to help with farming questions. Could you please rephrase your question?"
            except Exception as api_error:
                print(f"Gemini API error: {api_error}")
                print(f"API Key configured: {bool(settings.GEMINI_API_KEY)}")
                bot_response = f"I'm having trouble right now. Please ask about farming topics like crops or weather."
        
        print(f"Final response: {bot_response}")
        # Translation disabled for testing - will work in English for now
            
        return JsonResponse({'response': bot_response})
        
    except Exception as e:
        print(f"Chatbot error: {e}")  # For debugging
        error_msg = 'I apologize, but I\'m having trouble right now. Please try asking about farming, crops, weather, or agricultural practices.'
        return JsonResponse({'response': error_msg})