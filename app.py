import os
from flask import Flask, request, render_template
from mistralai.client import MistralClient
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
import subprocess
load_dotenv()
api_key = os.getenv('MISTRAL_API_KEY')

client = MistralClient(api_key=api_key)
llm = ChatMistralAI(model="codestral-latest", temperature=0, api_key=api_key)

app = Flask(__name__)

def assess_code_quality_python(code):
    pylint_output = subprocess.run(['pylint', '--disable=all', '--enable=style', '--output-format=json', '-'],
                                   input=code.encode('utf-8'),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   check=True)
    pylint_results = pylint_output.stdout.decode('utf-8')
    return pylint_results

import re

def is_code(input_text):
    """
    Checks if the input text should be treated as code.
    This function uses a combination of keyword detection and regex patterns
    to identify potential code snippets in Python, Java, C++, and JavaScript.
    """
    python_pattern = r'\b(def|class|if|for|while|import)\b'
    java_pattern = r'\b(public\s+static\s+void|class)\b'
    cpp_pattern = r'\b(#include\s*<.*>|int\s+main\s*\(\s*\)|class)\b'
    javascript_pattern = r'\b(function|class|let|const|var)\b'
    # Add more patterns for other languages as needed
    
    # Check for Python
    if re.search(python_pattern, input_text, re.IGNORECASE):
        return True
    # Check for Java
    elif re.search(java_pattern, input_text, re.IGNORECASE):
        return True
    # Check for C++
    elif re.search(cpp_pattern, input_text, re.IGNORECASE):
        return True
    # Check for JavaScript
    elif re.search(javascript_pattern, input_text, re.IGNORECASE):
        return True
    
    # Default to False if no recognized pattern is found
    return False


@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        if 'input' in request.form:
            input_text = request.form['input']
            # Determine if input_text is a question or code and process accordingly
            # Example:
            if is_code(input_text):
                response = assess_code_quality_python(input_text)
            else:
                llm_response = llm.invoke(["user", input_text])
                response = llm_response.content
            return response
        else:
            return 'Invalid request'
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

