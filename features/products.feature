Feature: The product store service back-end
    As an e-commerce website
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the server is started

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Product Demo REST API Service"
    And  I should not see "404 Not Found"