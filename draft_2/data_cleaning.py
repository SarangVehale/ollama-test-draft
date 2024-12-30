mport pandas as pd
import re
from PIL import Image
import pytesseract
from pytesseract import Output
from sklearn.impute import SimpleImputer
import numpy as np
import gc


def clean_text_data(text):
    """
    Normalize and clean text data.
    Removes unnecessary whitespace, non-alphanumeric characters, and fixes common OCR errors.
    """
    print("Cleaning text data...")
    try:
        text = re.sub(r'[^\w\s]', '', text)  # Remove non-alphanumeric characters
        text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
        return text
    except Exception as e:
        raise ValueError(f"Error cleaning text data: {str(e)}")


def clean_excel_data(dataframes):
    """
    Clean structured Excel data.
    Fills missing values, removes duplicates, and handles corrupted rows.
    """
    print("Cleaning Excel data...")
    try:
        cleaned_data = {}
        for sheet_name, df in dataframes.items():
            df.drop_duplicates(inplace=True)
            df.replace(r'^\s*$', np.nan, regex=True, inplace=True)  # Replace blank cells with NaN
            imputer = SimpleImputer(strategy="most_frequent")  # Impute missing data
            df[:] = imputer.fit_transform(df)
            cleaned_data[sheet_name] = df
        return cleaned_data
    except Exception as e:
        raise ValueError(f"Error cleaning Excel data: {str(e)}")


def enhance_image(image_path):
    """
    Enhance images to improve OCR performance.
    Converts images to grayscale and applies thresholding.
    """
    print("Enhancing image for OCR...")
    try:
        img = Image.open(image_path).convert("L")  # Convert to grayscale
        img = img.point(lambda x: 0 if x < 128 else 255, '1')  # Binarize the image
        return img
    except Exception as e:
        raise ValueError(f"Error enhancing image: {str(e)}")


def clean_cdr_data(dataframes):
    """
    Clean and normalize CDR data.
    Handles corrupted timestamps and fills missing fields.
    """
    print("Cleaning CDR data...")
    try:
        for key, df in dataframes.items():
            df.dropna(inplace=True)  # Drop rows with NaN
            if "call_time" in df.columns:
                df['call_time'] = pd.to_datetime(df['call_time'], errors='coerce')
            df = df[df['call_time'].notnull()]  # Remove rows with invalid timestamps
            dataframes[key] = df
        return dataframes
    except Exception as e:
        raise ValueError(f"Error cleaning CDR data: {str(e)}")


def clean_data(data):
    """
    Generic function to clean data based on its type.
    """
    if data["type"] == "text":
        cleaned_text = clean_text_data(data["data"])
        return {"type": "text", "data": cleaned_text}
    elif data["type"] == "structured":
        if isinstance(data["data"], dict):  # For multi-sheet Excel or CDR
            if "day_calls" in data["data"]:  # CDR-specific check
                cleaned_structured = clean_cdr_data(data["data"])
            else:
                cleaned_structured = clean_excel_data(data["data"])
        else:
            raise ValueError("Unsupported structured data format.")
        return {"type": "structured", "data": cleaned_structured}
    else:
        raise ValueError("Unsupported data type for cleaning.")


def main():
    while True:
        try:
            # Get file type and path
            file_type = input("\nEnter the file type you want to clean (text/excel/image/cdr): ").strip().lower()
            if file_type == "exit":
                print("Exiting cleaning program.")
                break

            file_path = input("Enter the path to the file to clean: ").strip()
            if not file_path:
                print("Invalid file path. Please try again.")
                continue

            # Process and clean based on type
            if file_type == "text":
                text = input("Enter the raw text to clean: ").strip()
                cleaned_data = clean_text_data(text)
                print("\nCleaned Text:", cleaned_data)

            elif file_type == "excel":
                excel_data = pd.read_excel(file_path, sheet_name=None)
                cleaned_data = clean_excel_data(excel_data)
                print("\nCleaned Excel Data:", cleaned_data.keys())

            elif file_type == "image":
                enhanced_image = enhance_image(file_path)
                text = pytesseract.image_to_string(enhanced_image, output_type=Output.STRING)
                cleaned_data = clean_text_data(text)
                print("\nExtracted and Cleaned Text from Image:\n", cleaned_data[:500])

            elif file_type == "cdr":
                cdr_data = pd.read_csv(file_path)
                cdr_dataframes = {"cdr": cdr_data}
                cleaned_data = clean_cdr_data(cdr_dataframes)
                print("\nCleaned CDR Data Keys:", cleaned_data.keys())

            else:
                print("Unsupported file type. Try again.")

        except Exception as e:
            print(f"Error: {e}")

        # Prompt for next action
        next_action = input("\nWould you like to clean another file? (yes/no): ").strip().lower()
        if next_action != "yes":
            print("Exiting cleaning program.")
            break

        # Garbage collection
        gc.collect()
        print("Memory cleaned up successfully.")

if __name__ == "__main__":
    main()

