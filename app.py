from flask import Flask, request, render_template, render_template_string
import os
from openai import AzureOpenAI

app = Flask(__name__)

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
    # Render the chat form using render_template
    return render_template('chat_form.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']
    conversation = [
        {"role": "system", "content": "You are an AI assistant that helps people find information."},
        {"role": "user", "content": user_message},
    ]

    response_data = get_chat_response_from_model(conversation)

    # Render the form again along with the response
    return render_template('chat_form.html', user_message=user_message, response=response_data)


def get_chat_response_from_model(chat_messages, model_name="Turbo35"):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=chat_messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == '__main__':
    app.run(debug=True)
