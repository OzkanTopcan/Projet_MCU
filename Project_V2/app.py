import pathlib
import sys

project_path = pathlib.Path(__file__).resolve().parents[0] 

if sys.path[0] != str(project_path):
    sys.path.insert(0, str(project_path)) 

from db import *
from setup import *

logger = setup_logging()

def get_sensor_values():   # TODO : dev this function
    """
    """
    # Testing values
    temp_close = 14
    temp_air = 14
    brightness = 75

    return temp_close, temp_air, brightness

def update_database(temp_close, temp_air, brightness):
    """
        Insert new values into db.
        Delete the old values/

        :param temp_close: The sensor value for close temperature.
        :type temp_close: int.
        :param temp_air: The sensor value for the brightness.
        :type temp_air: int.
        :param brightness: The sensor value for the brightness.
        :type brightness: int.
    """
    # Insert new values into db 
    insert_row_count = insert(temp_close, temp_air, brightness)
    if insert_row_count != 1:
        logger.error("Echec de l'insertion des donnees")
    else:
        logger.info("Succès de l'insertion des donnees")
    # Delete the old values
    delete_row_count = delete_old()
    if delete_row_count == 0:
        logger.info("Pas de donnees à supprimer")
    else:
        print("Donnees supprimee")
    return insert_row_count, delete_row_count

def generate_history():
    """
        Insert values in our table.

        :param records: Time of insertion.
        :type records: TimeStamp.
    """
    row_count, records = select_all()
    logger.info(f"Ecriture de {row_count} jeux de donnees dans history.txt")
    for row in records:
        # Create the set of data
        current = str(row[1])
        temp_close = str(row[2])
        temp_air = str(row[3])
        brightness = str(row[4])
        data = "current: " + current + ", temp_close: " + temp_close + ", temp_air: " + temp_air + ", brightness: " + brightness
        # Insert these datas into the file
        with open('history.txt', 'a') as fl:
            fl.write(data)
            fl.write("\n")
    logger.info("Fichier history.txt genere")

def run():
    """
        main function.
    """
    # Get values from arduino
    temp_close, temp_air, brightness = get_sensor_values
    # Update the data_base
    insert_row_count, delete_row_count = update_database(temp_close, temp_air, brightness)
    # Generate the history
    generate_history()