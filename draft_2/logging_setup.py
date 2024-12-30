mport logging
import os
from configparser import ConfigParser

# Read configuration file
config = ConfigParser()
config.read("config.json")

log_level = config.get("logging", "logging_level").upper()

# Create output directory if it doesn't exist
os.makedirs(config.get("paths", "output_file_path"), exist_ok=True)

# Setup logging configuration
logging.basicConfig(
    filename=os.path.join(config.get("paths", "output_file_path"), "app.log"),
    level=log_level,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to log errors
def log_error(message):
    logging.error(message)

