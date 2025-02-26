import csv
import random

def generate_humidity_csv(filename, num_rows=1000, min_value=30.0, max_value=90.0):
    """
    Generates a CSV file with a single column 'value' containing num_rows of random humidity values.
    
    :param filename: The name of the CSV file to create.
    :param num_rows: The number of data rows to generate.
    :param min_value: The minimum humidity value.
    :param max_value: The maximum humidity value.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["value"])  # Write header
        for _ in range(num_rows):
            # Generate a random humidity value rounded to 2 decimal places
            humidity = round(random.uniform(min_value, max_value), 2)
            writer.writerow([humidity])

# Generate the CSV file for AC humidity
generate_humidity_csv("ac_humidity.csv")

# Generate the CSV file for washing machine humidity
generate_humidity_csv("washing_humidity.csv")
