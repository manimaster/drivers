import os
import mysql.connector

class MySQLDB:
    def __init__(self):
        # Get MySQL connection details from ENV variables
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.port = int(os.getenv("MYSQL_PORT", 3306))
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASS", "")
        self.database = os.getenv("MYSQL_DB", "")

        self.connection = self._connect()
        self.cursor = self.connection.cursor()

    def _connect(self):
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return connection
    
    def execute_query(self, query, values=None):
        # Execute a SQL query
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def fetch_all(self):
        # Fetch all results from the last query
        return self.cursor.fetchall()

    def create_database(self, db_name):
        # Create a new database
        self.execute_query(f"CREATE DATABASE {db_name}")

    def delete_database(self, db_name):
        # Delete the specified database
        self.execute_query(f"DROP DATABASE {db_name}")

    def create_table(self, table_query):
        # Create a new table
        self.execute_query(table_query)

    def delete_table(self, table_name):
        # Delete the specified table
        self.execute_query(f"DROP TABLE {table_name}")

    def insert_record(self, table_name, columns, values):
        # Insert a new record into the table
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in values])})"
        self.execute_query(query, values)

    def get_records(self, table_name, where_clause=None):
        # Retrieve records from the table
        query = f"SELECT * FROM {table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
        self.execute_query(query)
        return self.fetch_all()

    def update_record(self, table_name, set_clause, where_clause):
        # Update a record in the table
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        self.execute_query(query)

    def delete_record(self, table_name, where_clause):
        # Delete a record from the table
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        self.execute_query(query)

    def close(self):
        # Close the connection
        self.cursor.close()
        self.connection.close()



# import os

# os.environ["MYSQL_HOST"] = "localhost"
# os.environ["MYSQL_PORT"] = "3306"
# os.environ["MYSQL_USER"] = "root"
# os.environ["MYSQL_PASS"] = "password"
# os.environ["MYSQL_DB"] = "testdb"


# db = MySQLDB()

# # Create a sample table
# create_table_query = """
# CREATE TABLE users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(255) NOT NULL,
#     age INT
# )
# """
# db.create_table(create_table_query)

# # Insert a sample record
# db.insert_record("users", ["username", "age"], ["john", 30])

# # Retrieve records
# print(db.get_records("users"))

# # Update a record
# db.update_record("users", "age=31", "username='john'")

# # Delete a record
# db.delete_record("users", "username='john'")

# db.close()
