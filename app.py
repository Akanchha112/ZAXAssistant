import os
from flask import Flask, request, render_template, jsonify
from mistralai.client import MistralClient
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()
api_key = os.getenv('MISTRAL_API_KEY')

client = MistralClient(api_key=api_key)
llm = ChatMistralAI(model="codestral-latest", temperature=0, api_key=api_key)

app = Flask(__name__)

code_keywords = [
    "code", "programming", "program", "wap", "algorithm", "data structure",
    "bug", "error", "debug", "fix", "issue", "problem",
    "java", "python", "c", "c++", "javascript", "ruby", "swift",
    "function", "method", "class", "object", "variable", "array",
    "loop", "conditional", "if", "else", "switch", "case",
    "string", "integer", "float", "boolean", "list", "dict",
    "database", "sql", "query", "table", "schema",
    "web", "development", "html", "css", "xml", "json",
    "api", "rest", "soap", "graphql", "http", "https",
    "oop", "object-oriented", "inheritance", "polymorphism",
    "design pattern", "architecture", "mvc", "mvvm",
    "testing", "unit test", "integration test", "debugging",
    "compiler", "interpreter", "IDE", "editor",
    "library", "framework", "module", "package",
    "exception", "try", "catch", "throw",
    "thread", "process", "concurrency", "parallel",
    "network", "socket", "tcp", "udp", "ip",
    "security", "vulnerability", "exploit", "patch",
    "optimization", "performance", "benchmark",
    "math", "statistics", "machine learning", "ai",
    "regex", "pattern", "matching", "validation",
    "type", "cast", "convert", "parse",
    "comment", "documentation", "README",
    "build", "compile", "deploy", "release",
    "version", "update", "patch", "fix",
    "dependency", "requirement", "installation",
    "environment", "setup", "configuration",
    "tool", "utility", "script", "automation",
    "error handling", "exception handling", "try-catch",
    "code review", "code smell", "refactoring",
    "agile", "scrum", "kanban", "waterfall",
    "UML", "diagram", "flowchart", "graph",
    "cloud", "aws", "azure", "google cloud", "cloud computing",
    "devops", "ci/cd", "continuous integration", "continuous deployment",
    "testing framework", "junit", "pytest", "unittest",
    "debugging tool", "gdb", "pdb", "debugger",
    "code analysis", "code metrics", "code quality",
    "code optimization", "code refactoring", "code review",
    "software development", "software engineering", "computer science",
]

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        data = request.get_json()
        question = data.get('question')
        code_to_document = data.get('code_to_document')

        if code_to_document:
            documentation_prompt = f"""
            Please generate comprehensive documentation for the following code:

            ```python
            {question}
            ```

            The documentation should include:

            - Function/Method descriptions
            - Parameter explanations
            - Return values
            - Example usage
            - Any other relevant information
            """

            llm_response = llm.invoke(["user", documentation_prompt])
            documentation = llm_response.content

            return jsonify({'response': documentation})
        else:
            for keyword in code_keywords:
                if keyword in question.lower():
                    llm_response = llm.invoke(["user", question])
                    response = llm_response.content
                    return jsonify({'response': response})
            return jsonify({'response': "Please enter a code-related query or code only."})
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
