import pandas  as pd 
import logging 

def read_the_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        
        logging.error(f"An error occurred while reading the data: {str(e)}")
    return df 

