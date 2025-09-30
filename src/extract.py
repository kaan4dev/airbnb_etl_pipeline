import os 
import pandas as pd

RAW_DATA_DIR = os.path.join("data", "raw")
RAW_DATA_FILE = os.path.join(RAW_DATA_DIR, "airbnb.csv")

def extract_airbnb_data(input_csv_path: str):
    os.makedirs(RAW_DATA_DIR, exist_ok = True)

    print(f"Reading raw data from {input_csv_path}")
    df = pd.read_csv(input_csv_path)

    print(f"Saving data to {RAW_DATA_FILE}")
    df.to_csv(RAW_DATA_FILE, index= False)

    return RAW_DATA_FILE

   
if __name__ == "__main__":
    input_path = "/Users/kaancakir/Downloads/archive (2)/AB_NYC_2019.csv"
    extract_airbnb_data(input_path)
