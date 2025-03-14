# Cypress AI plugin

Writing cypress tests used to be hard work. No more.

Instead of writing

    cy.get('#submit-button').click()

Just write this, and let the computer figure it out:

    cy.ai('click the submit button')

Or even more high level:

    cy.ai('visit amazon.com and order 5 pairs of socks using my credit card number #123-456-789')
    
How it works (full disclosure: it doesn't. This is joke, but I wouldn't mind if someone more talented made a proper implementation).

1. The cy.ai plugin sends your web page's html and your desired goal to the helper application.
2. The helper application uses fancy matrix magic (also known as an LLM) to write the actual cypress commands for you.
3. The cy.ai plugin executes the generated cypress commands and BOOM, you're done.

## Getting started

Install dependencies

    python -mvenv venv
    source venv/bin/activate
    pip install -r requirements
    ollama pull llama3:latest

    cd example
    npm install

Run the helper application

    python -m app.py

Open cypress and marvel at the example

    cd example
    npx cypress open

