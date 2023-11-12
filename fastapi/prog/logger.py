import os
from logging import Formatter, getLogger, handlers

LOGLEVEL = os.getenv("APP_LOGLEVEL", "INFO").upper()

# Create logger
logger = getLogger(__name__)
logger.setLevel(LOGLEVEL)

# Handler
LOG_FILE = "script.log"
handler = handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)

# Formatter
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)
