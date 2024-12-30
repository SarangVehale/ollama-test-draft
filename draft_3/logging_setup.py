import logging
import os
import json

# Read configuration file (config.json)
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Extract logging level from config and set it to uppercase
log_level = config.get("logging_level", "INFO").upper()

# Create output directory if it doesn't exist
os.makedirs(config.get("output_file_path", "./output/"), exist_ok=True)

# Set up logging configuration
logging.basicConfig(
    filename=os.path.join(config.get("output_file_path", "./output/"), "app.log"),
    level=log_level,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to log errors
def log_error(message):
    logging.error(message)

