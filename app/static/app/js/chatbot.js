// Standalone AI Chatbot Implementation
(function() {
    'use strict';
    
    // Create chatbot HTML
    const chatbotHTML = `
        <div id="ai-chatbot-container" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <!-- Floating Chat Button -->
            <button id="ai-chat-toggle-btn" type="button" aria-label="Open AI Assistant" style="
                width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #28a745, #20c997);
                border: none; color: white; font-size: 24px; cursor: pointer; box-shadow: 0 4px 20px rgba(40, 167, 69, 0.4);
                transition: all 0.3s ease; display: flex; align-items: center; justify-content: center;
            ">
                🤖
            </button>

            <!-- Chat Window -->
            <div id="ai-chat-window" style="
                display: none; position: absolute; bottom: 80px; right: 0; width: 350px; height: 500px;
                background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                overflow: hidden; flex-direction: column;
            ">
                <div id="ai-chat-header" style="
                    background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 15px 20px;
                    font-weight: 600; display: flex; align-items: center; justify-content: space-between;
                ">
                    <span>🤖 AI Farming Assistant</span>
                    <button id="ai-chat-close-btn" type="button" aria-label="Close chat" style="
                        background: none; border: none; color: white; font-size: 20px; cursor: pointer;
                        padding: 0; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;
                    ">×</button>
                </div>
                
                <div id="ai-chat-messages" style="
                    flex: 1; padding: 15px; overflow-y: auto; background: #f8f9fa; display: flex;
                    flex-direction: column; gap: 10px; max-height: 300px;
                ">
                    <div class="ai-chat-message ai-bot" style="
                        max-width: 85%; padding: 10px 15px; border-radius: 18px; font-size: 14px;
                        line-height: 1.4; word-wrap: break-word; background: #e9ecef; color: #333;
                        align-self: flex-start; border-bottom-left-radius: 5px;
                    ">
                        👋 Hello! I'm your AI farming assistant. Ask me about crops, weather, fertilizers, or any agricultural questions!
                    </div>
                </div>
                
                <div id="ai-chat-input-container" style="
                    padding: 15px; border-top: 1px solid #e0e0e0; display: flex; gap: 10px; background: white;
                ">
                    <input type="text" id="ai-chat-input" placeholder="Ask about farming..." maxlength="200" style="
                        flex: 1; border: 2px solid #e0e0e0; border-radius: 20px; padding: 10px 15px;
                        font-size: 14px; outline: none; transition: border-color 0.3s ease;
                    ">
                    <button id="ai-voice-btn" type="button" title="Voice Input" style="
                        background: #007bff; border: none; color: white; width: 40px; height: 40px;
                        border-radius: 50%; cursor: pointer; display: flex; align-items: center;
                        justify-content: center; transition: all 0.3s ease;
                    ">🎤</button>
                    <button id="ai-chat-send-btn" type="button" style="
                        background: #28a745; border: none; color: white; width: 40px; height: 40px;
                        border-radius: 50%; cursor: pointer; display: flex; align-items: center;
                        justify-content: center; transition: background-color 0.3s ease;
                    ">📤</button>
                </div>
            </div>
        </div>
    `;
    
    // Wait for DOM to load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChatbot);
    } else {
        initChatbot();
    }
    
    function initChatbot() {
        // Add chatbot to page
        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
        
        // Get elements
        const toggleBtn = document.getElementById('ai-chat-toggle-btn');
        const chatWindow = document.getElementById('ai-chat-window');
        const closeBtn = document.getElementById('ai-chat-close-btn');
        const chatInput = document.getElementById('ai-chat-input');
        const sendBtn = document.getElementById('ai-chat-send-btn');
        const voiceBtn = document.getElementById('ai-voice-btn');
        const messagesContainer = document.getElementById('ai-chat-messages');
        
        // Voice recognition setup
        let recognition = null;
        let isListening = false;
        
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';
        } else {
            voiceBtn.style.display = 'none';
        }
        
        // Toggle chat window
        toggleBtn.addEventListener('click', () => {
            if (chatWindow.style.display === 'none' || !chatWindow.style.display) {
                chatWindow.style.display = 'flex';
                chatInput.focus();
            } else {
                chatWindow.style.display = 'none';
            }
        });
        
        // Close chat window
        closeBtn.addEventListener('click', () => {
            chatWindow.style.display = 'none';
        });
        
        // Send message function
        function sendMessage() {
            const message = chatInput.value.trim();
            if (!message) return;
            
            // Add user message
            addMessage(message, 'user');
            chatInput.value = '';
            
            // Show typing indicator
            const typingMsg = addMessage('AI is thinking...', 'typing');
            
            // Disable send button
            sendBtn.disabled = true;
            
            // Send to backend
            const userLanguage = window.selectedLanguage || 'en';
            fetch('/ai-chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ 
                    message: message,
                    language: userLanguage
                })
            })
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data);
                console.log('Response text:', data.response);
                // Remove typing indicator
                typingMsg.remove();
                
                // Add bot response and speak it
                const botResponse = data.response || data.error || 'Sorry, I could not process your request.';
                addMessage(botResponse, 'bot');
                speakText(botResponse);
            })
            .catch(error => {
                console.error('Chatbot error:', error);
                // Remove typing indicator
                typingMsg.remove();
                
                // Add error message
                const errorMsg = `Connection error: ${error.message}. Please try again.`;
                addMessage(errorMsg, 'bot');
                speakText(errorMsg);
            })
            .finally(() => {
                sendBtn.disabled = false;
            });
        }
        
        // Add message to chat
        function addMessage(text, type) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `ai-chat-message ai-${type}`;
            
            const styles = {
                'user': 'background: #007bff; color: white; align-self: flex-end; border-bottom-right-radius: 5px;',
                'bot': 'background: #e9ecef; color: #333; align-self: flex-start; border-bottom-left-radius: 5px;',
                'typing': 'background: #e9ecef; color: #666; align-self: flex-start; font-style: italic;'
            };
            
            messageDiv.style.cssText = `
                max-width: 85%; padding: 10px 15px; border-radius: 18px; font-size: 14px;
                line-height: 1.4; word-wrap: break-word; ${styles[type]}
            `;
            
            messageDiv.textContent = text;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            return messageDiv;
        }
        
        // Voice input functionality
        if (recognition) {
            voiceBtn.addEventListener('click', () => {
                if (isListening) {
                    recognition.stop();
                } else {
                    recognition.start();
                }
            });
            
            recognition.onstart = () => {
                isListening = true;
                voiceBtn.style.background = '#dc3545';
                voiceBtn.textContent = '🔴';
                voiceBtn.title = 'Stop Recording';
            };
            
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                chatInput.value = transcript;
                sendMessage();
            };
            
            recognition.onend = () => {
                isListening = false;
                voiceBtn.style.background = '#007bff';
                voiceBtn.textContent = '🎤';
                voiceBtn.title = 'Voice Input';
            };
            
            recognition.onerror = () => {
                isListening = false;
                voiceBtn.style.background = '#007bff';
                voiceBtn.textContent = '🎤';
                voiceBtn.title = 'Voice Input';
            };
        }
        
        // Text-to-speech functionality
        function speakText(text) {
            if ('speechSynthesis' in window) {
                speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.9;
                utterance.pitch = 1;
                utterance.volume = 0.8;
                
                // Set language based on user selection
                const userLanguage = window.selectedLanguage || 'en';
                const speechLangMap = {
                    'hi': 'hi-IN', 'bn': 'bn-IN', 'te': 'te-IN', 'mr': 'mr-IN',
                    'ta': 'ta-IN', 'gu': 'gu-IN', 'kn': 'kn-IN', 'ml': 'ml-IN',
                    'pa': 'pa-IN', 'or': 'or-IN', 'as': 'as-IN', 'ur': 'ur-PK',
                    'ne': 'ne-NP', 'en': 'en-US'
                };
                
                utterance.lang = speechLangMap[userLanguage] || 'en-US';
                
                const voices = speechSynthesis.getVoices();
                const preferredVoice = voices.find(voice => 
                    voice.lang.startsWith(utterance.lang.split('-')[0]) ||
                    voice.lang === utterance.lang
                );
                if (preferredVoice) {
                    utterance.voice = preferredVoice;
                }
                
                speechSynthesis.speak(utterance);
            }
        }
        
        // Send button click
        sendBtn.addEventListener('click', sendMessage);
        
        // Enter key to send
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Input focus styling
        chatInput.addEventListener('focus', () => {
            chatInput.style.borderColor = '#28a745';
        });
        
        chatInput.addEventListener('blur', () => {
            chatInput.style.borderColor = '#e0e0e0';
        });
        
        // Hover effects
        toggleBtn.addEventListener('mouseenter', () => {
            toggleBtn.style.transform = 'scale(1.1)';
            toggleBtn.style.boxShadow = '0 6px 25px rgba(40, 167, 69, 0.6)';
        });
        
        toggleBtn.addEventListener('mouseleave', () => {
            toggleBtn.style.transform = 'scale(1)';
            toggleBtn.style.boxShadow = '0 4px 20px rgba(40, 167, 69, 0.4)';
        });
        
        sendBtn.addEventListener('mouseenter', () => {
            sendBtn.style.background = '#218838';
        });
        
        sendBtn.addEventListener('mouseleave', () => {
            sendBtn.style.background = '#28a745';
        });
    }
    
    // Get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
})();