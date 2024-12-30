import pandas as pd
import pdfplumber
from PIL import Image
import pytesseract
import os
import gc
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def process_excel(file_path):
    """Efficiently read Excel files into a dictionary of DataFrames."""
    try:
        logger.info("Processing Excel file...")
        excel_data = pd.read_excel(file_path, sheet_name=None)
        logger.info("Excel processing complete.")
        return {"type": "structured", "data": excel_data}
    except Exception as e:
        logger.error(f"Error processing Excel: {str(e)}")
        raise ValueError(f"Error processing Excel: {str(e)}")


def process_pdf(file_path):
    """Extract text from PDF files."""
    try:
        logger.info("Processing PDF file...")
        with pdfplumber.open(file_path) as pdf:
            text = "".join([page.extract_text() or "" for page in pdf.pages])
        logger.info("PDF processing complete.")
        return {"type": "text", "data": text.strip()}
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise ValueError(f"Error processing PDF: {str(e)}")


def process_image(image_path):
    """Extract text from image files using OCR."""
    try:
        logger.info("Processing Image file...")
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        logger.info("Image processing complete.")
        return {"type": "text", "data": text.strip()}
    except Exception as e:
        logger.error(f"Error processing Image: {str(e)}")
        raise ValueError(f"Error processing Image: {str(e)}")


def process_cdr(file_path):
    """Process Call Detail Record (CDR) files."""
    try:
        logger.info("Processing CDR file...")
        cdr_df = pd.read_csv(file_path)
        cdr_df['call_time'] = pd.to_datetime(cdr_df['call_time'], errors='coerce')
        cdr_df['time_of_day'] = cdr_df['call_time'].dt.hour.apply(
            lambda x: 'Day' if 6 <= x < 18 else 'Night' if pd.notna(x) else 'Unknown'
        )
        logger.info("CDR processing complete.")
        return {
            "type": "structured",
            "data": {
                "day_calls": cdr_df[cdr_df['time_of_day'] == 'Day'],
                "night_calls": cdr_df[cdr_df['time_of_day'] == 'Night']
            },
        }
    except Exception as e:
        logger.error(f"Error processing CDR: {str(e)}")
        raise ValueError(f"Error processing CDR: {str(e)}")


def detect_file_type(file_path):
    """Detect file type based on file extension."""
    file_extension = os.path.splitext(file_path)[-1].lower()
    logger.info(f"Detecting file type for: {file_path}")
    if file_extension in ['.xls', '.xlsx']:
        return "excel"
    elif file_extension == '.pdf':
        return "pdf"
    elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
        return "image"
    elif file_extension == '.csv':
        return "cdr"
    else:
        logger.error(f"Unsupported file type: {file_extension}")
        raise ValueError(f"Unsupported file type: {file_extension}")


def process_file(file_path):
    """Process file based on detected file type."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    file_type = detect_file_type(file_path)

    logger.info(f"Processing file of type: {file_type}")
    if file_type == "excel":
        return process_excel(file_path)
    elif file_type == "pdf":
        return process_pdf(file_path)
    elif file_type == "image":
        return process_image(file_path)
    elif file_type == "cdr":
        return process_cdr(file_path)
    else:
        logger.error(f"Unsupported file type: {file_type}")
        raise ValueError(f"Unsupported file type: {file_type}")


def main():
    while True:
        try:
            # Step 1: Get file path from user
            file_path = input("\nEnter the path to the file (or type 'exit' to quit): ").strip()
            if file_path.lower() == "exit":
                print("Exiting program.")
                break

            if not os.path.exists(file_path):
                print("Invalid file path. Please try again.")
                continue

            # Step 2: Process the file
            logger.info("\nDetecting file type...")
            result = process_file(file_path)

            # Step 3: Display basic information
            logger.info("Processing successful!")
            print("Data Type:", result["type"])
            if result["type"] == "text":
                print("Extracted Text (first 500 chars):\n", result["data"][:500])
            elif result["type"] == "structured":
                print("Structured Data Keys:", result["data"].keys())

        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"Error: {e}")

        # Step 4: Prompt for next action
        next_action = input("\nWould you like to process another file? (yes/no): ").strip().lower()
        if next_action != "yes":
            print("Exiting program.")
            break

        # Step 5: Garbage collection
        gc.collect()
        logger.info("Memory cleaned up successfully.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    main()

