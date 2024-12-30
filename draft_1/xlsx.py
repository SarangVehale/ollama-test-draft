mport pandas as pd

# Load the Excel file
def process_excel(file_path):
    excel_data = pd.read_excel(file_path, sheet_name=None)  # Load all sheets
    # You can choose a specific sheet if needed: sheet_name='Sheet1'

    for sheet_name, df in excel_data.items():
        # Process each sheet (for example, cleaning and analyzing)
        print(f"Processing sheet: {sheet_name}")
        print(df.head())
        # Apply further analysis or transformations if needed
    return excel_data

