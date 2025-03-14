from flask import Flask, request, jsonify

from ollama import Client

client = Client(
  host='http://localhost:11434',
  headers={'x-some-header': 'some-value'}
)

app = Flask(__name__)

@app.route('/cy-ai/next-step', methods=['POST'])
def get_next_cypress_step():
    print("getting next cypress step")
    # Get the HTML content from the request
    # Get the JSON data from the request
    data = request.get_json()
    # print("DATA", data)

    # Check if 'foo' and 'bar' are in the received data
    if 'html' not in data or 'goal' not in data:
        return jsonify({'error': 'Missing html_content or goal in request'}), 400

    # Process the HTML content (for example, calculate its length)
    content_length = len(data['html'])
    
    # Create a JSON response
    response = {
        'cy-ai-step': generate_cypress_command(data['html'], data['goal'])
    }

    print("XXX RESPONSE", response)
    return response

# Function to generate Cypress command
def generate_cypress_command(html_content, goal):
    is_simple = ask_is_simple(html_content, goal)
    print("goal is", "simple" if is_simple else "complex")

    if is_simple:
        command = get_cypress_command(html_content, goal)
        print("XXX Cypress command:", command)
        return command
    else:
        step = get_next_step(html_content, goal)
        print("XXX Next step:", step)
        command = get_cypress_command(html_content, step)
        print("XXX Cypress command:", command)
        return command

def get_next_step(html_content, goal):
    response = client.chat(model='llama3:latest', messages=[
        {
            'role': 'user',
            'content': f"""
            You are a test automation expert using Cypress. Given the following HTML content and a goal, you must break down
            the goal and determine the next small step the user should towards achieving the goal. 

            HTML Content:
            {html_content}

            Goal:
            {goal}

            It is important that you answer only with the next small step. If you include more information your answer will be rejected. The next step is:""",
        },
    ])

    step = response['message']['content']
    return step

def get_cypress_command(html_content, goal):
    response = client.chat(model='llama3:latest', messages=[
        {
            'role': 'user',
            'content': f"""
        You are a test automation expert using Cypress. Given the following HTML content and a goal, you should generate a cypress
        command that achieves the goal. Be very precise. If you use cy.get, then make sure the selector is unique. 
        
        HTML Content:
        {html_content}

        Goal:
        {goal}

        It is important that you answer only with the cypress command, otherwise your answer can not be parsed. Do not add quotes around your answer. Cypress command::""",
        },
    ])

    cypress_command = response['message']['content']
    return cypress_command

def ask_is_simple(html_content, goal):
    response = client.chat(model='llama3:latest', messages=[
        {
            'role': 'user',
            'content': f"""
    You are a test automation expert using Cypress. Given the following HTML content and a goal, you should determine if the goal
    can be achieved using a single cypress command. If it is possible, answer 'yes'. If it is complex or requires multiple cypress
    commands, answer with 'no'.

    HTML Content:
    {html_content}

    Goal:
    {goal}

    It is important that you answer only with yes or no, otherwise your answer cannot be parsed. Your answer:""",
        },
    ])

    if response['message']['content'].lower() == 'yes':
        return True
    if response['message']['content'].lower() == 'no':
        return False

    raise Exception("bad answer. todo: retry", response['message']['content'])

# Example usage
if __name__ == "__main__":
    # Sample HTML content and goal
    html_content = """
    <html>
        <body>
            <button id="submit-button">Submit</button>
            <input type="text" id="username" placeholder="Enter username" />
        </body>
    </html>
    """
    goal = "Click the submit button"

    # Generate the Cypress command
    cypress_command = generate_cypress_command(html_content, goal)
    print("Generated Cypress Command:")
    print(cypress_command)

    app.run(debug=True)


