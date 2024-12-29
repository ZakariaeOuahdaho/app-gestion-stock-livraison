import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection =mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='supermarche_db'
        )
        if connection.is_connected():
            print("connection reussi a la db")
            return connection
    except Error as e:
        print("errueur lor de la connection a la db")
        return None
    
def close_connection (connection):
    if connection.is_connected():
        connection.close()
        print("connexion a la db fermer")
    else:
        print("connection n a pas pu être intéronpu ")


#test 
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        close_connection(conn)