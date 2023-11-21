from flask import Flask, request, render_template, session, redirect, url_for
from flask_session import Session
import os
from openai import AzureOpenAI

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_KEY")

# Flas Session Configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up Azure OpenAI credentials
azure_endpoint = os.getenv("AZURE_OPENAI_CHAT_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_KEY")
api_version = "2023-05-15"

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=api_key,
    api_version=api_version
)

@app.route('/', methods=['GET'])
def index():
    # Render the chat form
    return render_template('chat_form.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']

    if 'conversation' not in session:
        session['conversation'] = [
            {"role": "system", "content": "You are an AI assistant that helps people find information."}
        ]

    session['conversation'].append({"role": "user", "content": user_message})

    response_text = get_chat_response_from_model(session['conversation'])
    formatted_response = response_text.replace("\n", "<br>")

    session['conversation'].append({"role": "assistant", "content": response_text})

    return render_template('chat_form.html', user_message=user_message, response=formatted_response)

def get_chat_response_from_model(chat_messages, model_name="Turbo35"):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=chat_messages
        )
        return response.choices[0].message.content if response.choices else "No response."
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/clear', methods=['GET'])
def clear_conversation():
    session.pop('conversation', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
