## Some useful commands for PostgresSQL

- ```createdb <database name>```
    - create a new postgress database on your local machine
- ```psql <database name>```
    - Open psql(PostgresSQL) command line tool, working within scope of your database.

### psql commands

- ```\dt```
    - list all tables for the current db
- ```\d+ <table name>```
    - list all columns for the given db
    
### Heroku Postgres Addon commands

- ```heroku pg:reset DATABASE_URL```
    - Heroku addon command that flushes the db in deployment