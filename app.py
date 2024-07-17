import os
from flask import Flask, request, render_template
from mistralai.client import MistralClient
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()
api_key = os.getenv('MISTRAL_API_KEY')

client = MistralClient(api_key=api_key)
llm = ChatMistralAI(model="codestral-latest", temperature=0, api_key=api_key)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        question = request.form['question']
        # Interact with the Mistral AI model
        llm_response = llm.invoke(["user", question])
        response = llm_response.content  # Accessing the 'content' attribute directly
        return response
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
