from pyhive import hive
import time

# Hive connection parameters
hive_host = 'hive-server'
hive_port = 10000
hive_database = 'yolo'

# Create a connection to Hive
conn = hive.Connection(
    host=hive_host,
    port=hive_port,
    database=hive_database
)

# Create a cursor
# Le cursor permet de deplacer dans la base de donnes et d'executer des requetes
cursor = conn.cursor()

# Create a Hive table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS users (
    id STRING,
    nom STRING,
    prenom STRING,
    age INT,
    email STRING,
    preferences ARRAY<STRING>,
    solde FLOAT,
    ne INT
)
STORED AS PARQUET
"""
cursor.execute(create_table_query)

# Example user data
user_data = [
    ('1', 'Dupont', 'Jean', 30, 'jean.dupont@example.com', ['sports', 'music'], 2500.75, 3),
    ('2', 'Martin', 'Marie', 25, 'marie.martin@example.com', ['tech', 'travel'], 3200.00, 2),
    ('3', 'Durand', 'Pierre', 40, 'pierre.durand@example.com', ['cooking', 'hiking'], 4200.50, 4)
]

# Insert user data into the Hive table
insert_query = """
INSERT INTO users (id, nom, prenom, age, email, preferences, solde, ne)
VALUES ('{}', '{}', '{}', {}, '{}', {}, {}, {})
"""
for user in user_data: # array('sports','music')
    formatted_preferences = "array(" + ",".join("'{}'".format(p) for p in user[5]) + ")"
    formatted_query = insert_query.format(user[0], user[1], user[2], user[3], user[4], formatted_preferences, user[6], user[7])
    cursor.execute(formatted_query)


# Close the cursor and connection
cursor.close()
conn.close()

print("User data inserted successfully into Hive table.")
