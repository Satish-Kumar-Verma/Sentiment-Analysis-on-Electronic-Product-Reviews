import os
import csv
import pickle

# Paths
DATA_DIR = os.path.join(os.getcwd(), "data")
SENTIMENT_OUTPUT_PATH = os.path.join(DATA_DIR, "sentiment_output.csv")

products_without_price = []

# Go through the sentiment_output.csv
with open(SENTIMENT_OUTPUT_PATH, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip the header row
    i = 1
    for row in reader:
        product_path = row[3]
        
        # Determining path for specifications based on the product path
        SPEC_PATH = os.path.join(DATA_DIR, product_path.lstrip("data\\"), "specifications.bin")
        
        # Unpickling the specifications.bin file
        with open(SPEC_PATH, "rb") as spec_file:
            spec_data = pickle.load(spec_file)
            specifications_dict = spec_data[1]  # Grabbing only the specifications dictionary

        # Check for "Price" key and nested "Original" and "Discount" keys
        if "Price" not in specifications_dict or \
           "Original" not in specifications_dict["Price"] or \
           "Discount" not in specifications_dict["Price"]:
            products_without_price.append(row[4])  # append product name

        else:
            print(f'{i}. {specifications_dict["Price"]}')
            # print(f'{float(specifications_dict["Price"]["Original"].replace("₹", "").replace(",", ""))}')
            i += 1

# Output products without price
if products_without_price:
    print("Products without proper price values:")
    for product in products_without_price:
        print(product)
else:
    print("All products have proper price values.")
