# products
[![Build Status](https://travis-ci.org/stern-devops-2020-products/products.svg?branch=master)](https://travis-ci.org/stern-devops-2020-products/products)

The products resource represents the store items that the customer can buy. They could be categorized but they don’t have to be for this assignment. They should have a unique id (perhaps a SKU - Stock Keeping Unit), a name, description, price, and others attributes like perhaps an image. 

## Table Schema
- id (integer)
- name (string, length of 63)
- sku (string, length of 14)
- available (boolean)
- price (float)
- stock (integer)
- size (string, length of 4)
- color (string, length of 10)
- category (string, length of 63)
- description (string, length of 250)
- lastUpdated (string, length of 10)

## Services Descriptions
Please see below for the API endpoints available through the products service.
- Create a product: POST /products
- Read/retrieve a product: GET /products/<<int:product_id>>
- Update a product: PUT /products/<<int:product_id>>
- Delete a product: DELETE /products/<<int:product_id>>
- List all products: GET /products

## PostgreSQL
This service utilizes a PostgreSQL database hosted within a docker container. 

You can access the database from inside vagrant by the following command and using the password "postgres":
```
psql -h localhost -U postgres -d postgres
```
To run a query use the following to execute a query in the query.txt file once at the postgres=# prompt
```
\i query.txt
```
Alternatively, you can access the database directly from inside docker using:
```
docker exec -it postgres psql -U postgres
```
