Feature: The product store service back-end
    As an e-commerce website
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | sku      | price     | stock      | size     | color     | category      | description       | available     |
        | Nike       | 345903   | 34.99     | 10         | S        | Pink      | sweatshirt    | Nike sweatshirt   | True          | 
        | Pants      | 345890   | 20.00     | 80         | M        | Black     | pants         | Nike pants        | True          | 
        

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Products" in the title
    And  I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Kevin"
    And I set the "SKU" to "KJA324"
    And I set the "Price" to "69.42"
    And I set the "Stock" to "33"
    And I set the "Size" to "L"
    And I set the "Color" to "Blue"
    And I set the "Category" to "People"
    And I set the "Description" to "Best person ever"
    And I select "True" in the "Available" dropdown
    And I press the "Create" button
    Then I should see the message "Product Created"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "SKU" field should be empty
    And the "Price" field should be empty
    And the "Stock" field should be empty
    And the "Size" field should be empty
    And the "Color" field should be empty
    And the "Category" field should be empty
    And the "Description" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Kevin" in the "Name" field
    And I should see "KJA324" in the "SKU" field
    And I should see "69.42" in the "Price" field
    And I should see "33" in the "Stock" field
    And I should see "L" in the "Size" field
    And I should see "Blue" in the "Color" field
    And I should see "People" in the "Category" field
    And I should see "Best person ever" in the "Description" field
    And I should see "True" in the "Available" dropdown

    Scenario: List All Products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "Nike" in the results
    And I should not see "Scott" in the results
    
