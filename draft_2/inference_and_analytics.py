import pandas as pd
import requests
import gc
import json
import logging
from tabulate import tabulate

# Load configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Set up logging
logging.basicConfig(
    level=getattr(logging, config.get("logging_level", "INFO").upper()),
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def infer_text_data(text):
    """
    Use the Ollama model to infer insights from text data via local API.
    """
    logger.info("Running inference on text data...")
    try:
        response = requests.post(
            url=f"{config['ollama_api_url']}/chat",
            json={"prompt": text},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()["text"].strip()
    except requests.RequestException as e:
        logger.error(f"Error during text inference: {str(e)}")
        raise ValueError(f"Error during text inference: {str(e)}")

def generate_analytics(data):
    """
    Generate analytics for structured data (Excel, CDR).
    """
    logger.info("Generating analytics for structured data...")
    try:
        analytics_results = {}
        for key, df in data.items():
            stats = {
                "Row Count": len(df),
                "Column Count": len(df.columns),
                "Missing Values": df.isnull().sum().to_dict(),
                "Sample Data": df.head().to_dict(orient="records")
            }
            analytics_results[key] = stats
        return analytics_results
    except Exception as e:
        logger.error(f"Error during analytics generation: {str(e)}")
        raise ValueError(f"Error during analytics generation: {str(e)}")

def infer_and_analyze(data):
    """
    Main inference and analytics function.
    """
    logger.info("Starting inference and analytics process...")
    if data["type"] == "text":
        return {"type": "text", "output": infer_text_data(data["data"])}
    elif data["type"] == "structured":
        return {"type": "analytics", "output": generate_analytics(data["data"])}
    else:
        raise ValueError("Unsupported data type for inference or analytics.")

def display_results(results):
    """
    Display inference or analytics results to the user.
    """
    logger.info("Displaying results...")
    print("\nResults:")
    if results["type"] == "text":
        print("Text Inference:\n", results["output"])
    elif results["type"] == "analytics":
        for sheet_name, analytics in results["output"].items():
            print(f"\n--- Analytics for {sheet_name} ---")
            print(f"Row Count: {analytics['Row Count']}")
            print(f"Column Count: {analytics['Column Count']}")
            print("Missing Values:")
            print(tabulate(analytics["Missing Values"].items(), headers=["Column", "Missing Values"]))
            print("Sample Data:")
            print(tabulate(analytics["Sample Data"], headers="keys", tablefmt="grid"))
    else:
        print("Unsupported result type.")

def main():
    while True:
        try:
            # Prompt user for data type
            data_type = input("\nEnter the data type for inference (text/structured): ").strip().lower()
            if data_type == "exit":
                logger.info("Exiting inference program.")
                break

            if data_type == "text":
                # Handle text inference
                text = input("Enter the text to analyze: ").strip()
                data = {"type": "text", "data": text}
                results = infer_and_analyze(data)
                display_results(results)

            elif data_type == "structured":
                # Handle structured data analytics
                file_path = input("Enter the path to the cleaned structured data file (CSV/Excel): ").strip()
                if file_path.endswith(".csv"):
                    df = pd.read_csv(file_path)
                    data = {"type": "structured", "data": {"sheet1": df}}
                elif file_path.endswith(".xls") or file_path.endswith(".xlsx"):
                    df_dict = pd.read_excel(file_path, sheet_name=None)
                    data = {"type": "structured", "data": df_dict}
                else:
                    print("Unsupported file format. Please use CSV or Excel.")
                    continue

                results = infer_and_analyze(data)
                display_results(results)

            else:
                print("Unsupported data type. Please try again.")

        except Exception as e:
            logger.error(f"Error: {e}")

        # Prompt for next action
        next_action = input("\nWould you like to analyze another dataset? (yes/no): ").strip().lower()
        if next_action != "yes":
            logger.info("Exiting inference program.")
            break

        # Garbage collection
        gc.collect()
        logger.info("Memory cleaned up successfully.")

if __name__ == "__main__":
    main()

