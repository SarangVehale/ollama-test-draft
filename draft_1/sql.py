mport sqlite3

def process_sql_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Example: Query a table
    cursor.execute("SELECT * FROM calls")
    rows = cursor.fetchall()
    
    # Convert rows to DataFrame for easier processing
    df = pd.DataFrame(rows, columns=[col[0] for col in cursor.description])
    
    conn.close()
    return df

