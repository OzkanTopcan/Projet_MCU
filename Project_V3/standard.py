from db import *
import os

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
        with open('static/history.txt', 'a', encoding="utf-8") as fl:
            fl.write(data)
            fl.write("\n")
    logger.info("Fichier history.txt genere")
