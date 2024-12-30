import argparse
import logging
import os
import sys
import gc
from file_processing import process_file  # Updated to match your current structure
from data_cleaning import clean_data
from inference_and_analytics import infer_and_analyze, display_results
from logging_setup import log_error

def parse_args():
    """Parse command-line arguments for the pipeline."""
    parser = argparse.ArgumentParser(description="Data Processing Pipeline")
    parser.add_argument("file_path", type=str, help="Full path to the file to be processed")
    return parser.parse_args()

def run_pipeline():
    """Main pipeline to process and analyze data."""
    try:
        # Step 1: Parse arguments
        args = parse_args()
        file_path = args.file_path

        # Step 2: Validate file path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Step 3: Process the file (detect type and read content)
        logging.info(f"Processing file: {file_path}")
        raw_data = process_file(file_path)

        # Step 4: Clean the data
        logging.info("Cleaning data...")
        cleaned_data = clean_data(raw_data)

        # Step 5: Run inference and analytics
        logging.info("Running inference and analytics...")
        results = infer_and_analyze(cleaned_data)

        # Step 6: Display results
        logging.info("Displaying results...")
        display_results(results)

        # Step 7: Garbage collection
        gc.collect()
        logging.info("Memory cleaned up successfully.")

    except Exception as e:
        # Log and handle errors
        error_message = f"Error occurred: {str(e)}"
        logging.error(error_message)
        log_error(error_message)
        sys.exit(1)

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("pipeline.log"),  # Logs to file
            logging.StreamHandler(sys.stdout)    # Logs to console
        ]
    )
    run_pipeline()
