/// <reference types="cypress" />

describe('visit-paul', () => {
  beforeEach(() => {
    cy.visit('https://swapi.dev/')
  })

  it('find paul and visit his github profile', () => {
    cy.ai('click the documentation link')
    cy.ai('click the elixir link')
  })
})
