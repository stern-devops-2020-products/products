# products
The products resource represents the store items that the customer can buy. They could be categorized but they don’t have to be for this assignment. They should have a unique id (perhaps a SKU - Stock Keeping Unit), a name, description, price, and others attributes like perhaps an image. 

## PostgreSQL
This service utilizes a PostgreSQL database hosted within a docker container. 

You can access the database from inside vagrant by the following command and using the password "postgres":
---
psql -h localhost -U postgres -d postgres
---

To run a query use the following to execute a query in the query.txt file once at the postgres=# prompt
---
\i query.txt
---

Alternatively, you can access the database directly from inside docker using:
---
docker exec -it postgres psql -U postgres
---
