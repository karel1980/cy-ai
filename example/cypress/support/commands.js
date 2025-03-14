// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

Cypress.Commands.add('ai', (goal) => {
  const pageHtml = Cypress.$('html').prop('outerHTML');

  // The cy-ai backend endpoint
  const endpointUrl = 'http://127.0.0.1:5000/cy-ai/next-step';

  console.log('Asking the AI backend for the next step to achieve the goal:', goal)
  return cy.request({
    method: 'POST',
    url: endpointUrl,
    body: {
      html: pageHtml,
      goal: goal,
    },
    headers: {
      'Content-Type': 'application/json',
    },
  }).then((response) => {
    // Log the response
    cy.log('Response:', JSON.stringify(response));
    const step = response.body['cy-ai-step']
    cy.log('The AI backend suggests this cypress command:', step)
    eval(response.body['cy-ai-step'])
    cy.log('I have evaluated the suggested command:', step)
  });
});
