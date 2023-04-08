import os
import uuid
import configparser
import openai
from flask import Flask, request, jsonify

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the API key from the config file, or fallback to the environment variable
api_key = config.get('openai', 'api_key', fallback=os.getenv("OPENAI_API_KEY"))

if api_key == "YOUR_API_KEY" or not api_key:
    raise ValueError("API key not found in config file or environment variable")
print(api_key)
app = Flask(__name__)
chat_sessions = {}

openai.api_key = api_key


@app.route('/api/sessions', methods=['POST'])
def create_session():
    session_id = str(uuid.uuid4())
    chat_sessions[session_id] = []
    return jsonify({"session_id": session_id})


@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    return jsonify(list(chat_sessions.keys()))


@app.route('/api/sessions/<session_id>/history', methods=['GET'])
def get_chat_history(session_id):
    if session_id not in chat_sessions:
        return jsonify({"error": "Invalid session_id"}), 400

    return jsonify(chat_sessions[session_id])


@app.route('/api/sessions/<session_id>/chat', methods=['POST'])
def chat(session_id):
    data = request.get_json()
    user_input = data.get('message', '')

    if session_id not in chat_sessions:
        return jsonify({"error": "Invalid session_id"}), 400

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response = generate_response(user_input)
    chat_sessions[session_id].append({"user": user_input, "bot": response})

    return jsonify({"response": response})


@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    if session_id not in chat_sessions:
        return jsonify({"error": "Invalid session_id"}), 400

    del chat_sessions[session_id]
    return jsonify({"status": "success"})


def generate_response(prompt):
    model_engine = "text-davinci-002"

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    generated_text = response.choices[0].text.strip()
    return generated_text


if __name__ == "__main__":
    app.run(debug=True)
