import logging
from logging.handlers import RotatingFileHandler
import os

# Ottieni la cartella corrente
current_directory = os.getcwd()
file_log = os.path.join(current_directory, 'log/app.log')

# crea il logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# formattazione dei log
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# creo l'handler per gestire il logrotate
logrotate = RotatingFileHandler(
    filename=file_log,
    maxBytes=20000,
    backupCount=3
    )
logrotate.setFormatter(formatter)

# aggiungo l'handler per gestire la scrittura dei log e i logrotate
logger.addHandler(logrotate)