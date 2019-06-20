import mysql.connector as mariadb
from setup import *
from binary import *

logger = setup_logging()


def connect():
    """
        Make the connection to MariaDB.
        :returns: The connection object.
        :rtype: object.
    """
    try:
        # DB connection
        logger.info("[O] Connection a la base de donnees")
        mySQLconnection = mariadb.connect(
            database='project_mcu',
            user='ozkan',
            password='ozkan'
        )
        logger.info("[O] Succes de la connection a la base de donnees")
    except Exception as error :
        logger.error("[X] Echec de la connection a la base de donnees")
        logger.error("Connection error : {}".format(error))
        
    return mySQLconnection

def insert(temp_close, temp_air, brightness):
    """
        Insert values in our table.

        :param temp_close: The sensor value for close temperature.
        :type temp_close: int.
        :param temp_air: The sensor value for the brightness.
        :type temp_air: int.
        :param brightness: The sensor value for the brightness.
        :type brightness: int.
        :returns: The rowcount.
        :rtype: int.
    """
    # Conncect to DB
    connection = connect()
    try:
        logger.info("[O] Insertion de donnees")
        # Initializations
        cursor = connection.cursor(buffered=True)
        request = "INSERT INTO historique (temp_close, temp_air, brightness) VALUES (%s, %s, %s)"
        values = (temp_close, temp_air, brightness)
        # Execute request
        cursor.execute(request, values)
        connection.commit()
        logger.info("[O] Succes de la requete, {} ligne(s) inseree".format(cursor.rowcount))
    # Handle error
    except Exception as error :
        logger.error("[X] Echec de la requete : {}".format(error))
    finally:
        # Closing database connection.
        if(connection.is_connected()):
            connection.close()
            print("Connectionclosed")
    
    return cursor.rowcount

def select_all():
    """
        Select all the values in our table.

        :returns: The rowcount, the query result.
        :rtype: tuple(int, list[list]).
    """
    # Conncect to DB
    connection = connect()
    try:
        logger.info("[O] Recuperation de l'ensemble des donnees de la table")
        # Initializations
        records = None
        cursor = connection.cursor(buffered=True)
        request = "SELECT * from historique"
        # Execute request
        cursor.execute(request)
        connection.commit()
        logger.info("[O] Succes de la requete, {} ligne(s) recuperee".format(cursor.rowcount))
        records = cursor.fetchall()
    # Handle error
    except Exception as error :
        logger.error("[X] Connection error : {}".format(error))
    finally:
        # Closing database connection.
        if(connection.is_connected()):
            connection.close()
            print("Connectionclosed")

    return cursor.rowcount, records

def delete_old():
    """
            Delete old values of our table.

            :returns: The rowcount.
            :rtype: int.
    """
    # Conncect to DB
    connection = connect()
    try:
        logger.info("[O] Suppression des donnees datant de plus d'1 semaine")
        # Initializations
        cursor = connection.cursor(buffered=True)
        request = 'DELETE FROM historique WHERE TIMEDIFF(CURRENT_TIMESTAMP, current) > "07:00:00"'
        # Execute request
        cursor.execute(request)
        connection.commit()
        logger.info("[O] Succes de la requete, {} ligne(s) effacee".format(cursor.rowcount))
    # Handle error
    except Exception as error :
        logger.error("[X] Echec de la requete : {}".format(error))
    finally:
        # Closing database connection.
        if(connection.is_connected()):
            connection.close()
            print("Connectionclosed")

    return cursor.rowcount

def truncate():  # TODO : Call in API !!!!
    """
            Truncate our table.

            :returns: The rowcount.
            :rtype: int.
    """
    # Conncect to DB
    connection = connect()
    try:
        logger.info("[O] Suppression de toutes les donnees")
        # Initializations
        cursor = connection.cursor(buffered=True)
        request = "TRUNCATE TABLE historique"
        # Execute request
        cursor.execute(request)
        connection.commit()
        logger.info("[O] Succes de la requete, table vide")
    # Handle error
    except Exception as error :
        logger.error("[X] Echec de la requete : {}".format(error))
    finally:
        # Closing database connection.
        if(connection.is_connected()):
            connection.close()
            print("Connectionclosed")

    return cursor.rowcount

def select_current():
    """
        Select the latest values in our table.

        :returns: The rowcount, the query result.
        :rtype: tuple(int, list[list]).
    """
    # Conncect to DB
    connection = connect()
    try:
        logger.info("[O] Recuperation de l'ensemble des donnees de la table")
        # Initializations
        records = None
        cursor = connection.cursor(buffered=True)
        request = "SELECT * FROM historique ORDER BY ID DESC LIMIT 1;"
        # Execute request
        cursor.execute(request)
        connection.commit()
        logger.info("[O] Succes de la requete, {} ligne(s) recuperee".format(cursor.rowcount))
        records = cursor.fetchall()
    # Handle error
    except Exception as error :
        logger.error("[X] Connection error : {}".format(error))
    finally:
        # Closing database connection.
        if(connection.is_connected()):
            connection.close()
            print("Connectionclosed")

    return cursor.rowcount, records


#insert(temp_close="14", temp_air="56", brightness="88")
#insert(temp_close="15", temp_air="26", brightness="77")
#insert(temp_close="14", temp_air="136", brightness="68")
#insert(temp_close="16", temp_air="16", brightness="77")
#insert(temp_close="19", temp_air="36", brightness="73")
#insert(temp_close="17", temp_air="56", brightness="75")
#select_all()
#truncate()
#delete_old()
#-
# 
# 
# .
# a, b = select_current()
