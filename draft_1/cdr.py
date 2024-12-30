mport pandas as pd

def process_cdr(file_path):
    cdr_df = pd.read_csv(file_path)
    
    # Convert call time to datetime
    cdr_df['call_time'] = pd.to_datetime(cdr_df['call_time'])
    # Categorize calls as Day or Night
    cdr_df['time_of_day'] = cdr_df['call_time'].dt.hour.apply(lambda x: 'Day' if 6 <= x < 18 else 'Night')
    
    # Example query: Day vs Night calls
    day_calls = cdr_df[cdr_df['time_of_day'] == 'Day']
    night_calls = cdr_df[cdr_df['time_of_day'] == 'Night']
    
    return day_calls, night_calls

