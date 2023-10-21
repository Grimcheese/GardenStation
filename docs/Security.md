# Information Security
This project is being developed with cyber security principles in mind and serves as a learning tool for getting a better understanding of how to manage the requirements of a solution in a way that allows accessibility without compromising on the security of data and resources of a system.

# The Database
In many web applications Databases are often the main target of an attack. This is due to the fact that they often contain large amounts of valuable data and there are many vulnerabilities that can allow malicious actors to access them. In desigining my database I have considered these factors and researched the best way to secure the database in order to create a secure implementation.

I chose to use SQLite as the DBMS as it is lightweight but still has many of the features and fucntions of larger systems such as MySQL or MongoDB. Python also has a sqlite3 library installed in the standard installation making it easy to begin development on.

## Security Considerations
The main areas to consider in securing the database are:
- User supplied values for queries
- How output from the database is displayed to the user
- Physical access of the database

To ensure that users are unable to insert valid SQL commands when selecting data, parameterised queries are used. This ensures that any data that is to be inserted into a query is only considered as data and is not inserted into the SQL query as a String literal without escaping. 