import os
import csv

def load_bs_years_data(file_path):
    bs_years_data = {}
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            year = int(row[0])  # The first column is the year
            months_data = [int(x) for x in row[1:]]  # The rest are the months' data
            bs_years_data[year] = months_data
    return bs_years_data

# Get the absolute path of the CSV file in the `converter` app
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'calendar_bs.csv')

# Load the CSV data into a dictionary
bs_years_data = load_bs_years_data(file_path)

