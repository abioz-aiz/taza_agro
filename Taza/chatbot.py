from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def test_llm_server(input_text):
    """Simple response function for testing"""
    try:
        # Add your chatbot logic here
        # For testing, we'll return a simple response
        responses = {
            "hello": "Hi! How can I help you today?",
            "how are you": "I'm doing well, thank you! How can I assist you?",
            "price": "I can help you predict crop prices. What crop are you interested in?",
            "weather": "I can provide weather information. Which city would you like to know about?"
        }
        
        # Convert input to lowercase for matching
        input_lower = input_text.lower()
        
        # Find matching response or return default
        for key in responses:
            if key in input_lower:
                return responses[key]
                
        return "I'm here to help with crop prices and weather information. What would you like to know?"
        
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

@app.route('/v1/chat/completions', methods=['POST'])
def chat():
    try:
        data = request.json
        input_text = data['messages'][0]['content']
        response = test_llm_server(input_text)
        
        return jsonify({
            "choices": [{
                "message": {
                    "content": response
                }
            }]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting chatbot server on http://localhost:1234")
    app.run(port=1234, debug=True)
