import pathlib
import sys
import time
import serial
import os

project_path = pathlib.Path(__file__).resolve().parents[0] 

if sys.path[0] != str(project_path):
    sys.path.insert(0, str(project_path)) 

from db import *
from setup import *
from binary import *

logger = setup_logging()

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

def generate_history():  # TODO : call in API !!!
    """
        Insert values in our table.

        :param records: Time of insertion.
        :type records: TimeStamp.
    """
    try:
        os.remove(history.txt)
    except Exception as error:
        print(error)
    row_count, records = select_all()
    logger.info("Ecriture de {} jeux de donnees dans history.txt".format(row_count))
    for row in records:
        # Create the set of data   TODO : Check Tuple !!!!
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
    # Initialize connedctions
    ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )
    # Initialize variables
    count = 0
    next_value = ""
    temp_close = ""
    temp_air = ""
    brightness = ""
    # Infinite loop  # TODO: handle keyboard interrupt
    while True:
        # Get value on serial port
        value = ser.readline()
        if len(value) == 5:
            # We received the recongnition bytes, Conversion
            str_value = str(value[0:3])
            decimal_value = binairedecimal(str_value)
            # To know which sensor we're dealing with
            if decimal_value == 4:
                next_value = "temp_close"
                print("temp_close1")
            elif decimal_value == 5:
                next_value = "temp_air"
                print("temp_air1")
            elif decimal_value == 6:
                next_value = "brightness"
                print("temp_bright1")
        elif len(value) == 10:
            # We received the body, Conversion
            str_value = str(value[0:13])
            decimal_value = binairedecimal(str_value)
            # Getting the values 
            if next_value == "temp_close":
                temp_close = decimal_value
                print("temp_close2")
                count += 1
            elif next_value == "temp_air":
                temp_air = decimal_value
                print("temp_air2")
                count += 1
            elif next_value == "brightness":
                brightness = decimal_value
                print("temp_bright2")
                count += 1
        # We received all the values, update databases
        if count == 3:
            print("3 valeurs")
            count = 0
            next_value = ""
            # Update the data_base
            update_database(temp_close, temp_air, brightness)
            temp_close = ""
            temp_air = ""
            brightness = ""
            
run()
            
