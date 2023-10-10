import pandas as pd
import logging
from dotenv import load_dotenv
import os


logging.basicConfig(level=logging.ERROR)  


load_dotenv()


raw_file_path = os.environ.get("MY_FILE_PATH")

if raw_file_path:
    
    file_path = eval(raw_file_path)

    try:
        with open(file_path, "r") as file:
            data = file.read()
        print(f"File data: {data}")
    except Exception as e:
        logging.error(f"An error occurred while reading the data: {str(e)}")
else:
    print("Environment variable MY_FILE_PATH is not set.")


def read_the_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        logging.error(f"An error occurred while reading the data: {str(e)}")
        return None


if __name__ == "__main__":
    data_frame = read_the_data(file_path)
    if data_frame is not None:
        # You can do something with the DataFrame here, like printing it or performing operations.
        print(data_frame.head())