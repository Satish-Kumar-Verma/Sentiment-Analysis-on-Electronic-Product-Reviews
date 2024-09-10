import os
import csv
import pickle
import json

# Setting up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recommendation_system.settings")

import django
django.setup()

from products.models import Product

# Paths
DATA_DIR = os.path.join(os.getcwd(), "data")
# STATIC_DIR = os.path.join(os.getcwd(), 'static')
SENTIMENT_OUTPUT_PATH = os.path.join(DATA_DIR, "sentiment_output.csv")

# Populating the database
with open(SENTIMENT_OUTPUT_PATH, 'r') as f:
    reader = csv.reader(f)
    total_rows = sum(1 for row in f) - 1  # Get total rows minus the header
    f.seek(0)  # Reset file pointer after counting rows
    next(reader)  # skip the header row

    i = 1
    for row in reader:
        try:
            product_model = row[0]
            positive_percentage = float(row[1])
            negative_percentage = float(row[2])
            product_path = row[3]

            # Determining paths for specifications and image based on the product path
            SPEC_PATH = os.path.join(DATA_DIR, product_path.lstrip("data\\"), "specifications.bin")
            IMAGE_PATH = os.path.join(product_path, "image.jpeg")

            # Unpickling the specifications.bin file to get product name and specifications
            with open(SPEC_PATH, "rb") as spec_file:
                spec_data = pickle.load(spec_file)
                specifications_dict = spec_data[1]  # Grabbing only the specifications dictionary


            # Extracting prices from the specifications
            try:
                discount_price = float(specifications_dict["Price"]["Discount"].replace("₹", "").replace(",", ""))
                original_price = float(specifications_dict["Price"]["Original"].replace("₹", "").replace(",", ""))
            except ValueError:
                original_price = discount_price

            # Convert the specifications dictionary to JSON for storage in the database
            specifications_json = json.dumps(specifications_dict)

            # Using Django's ORM to create or update the product in the database
            product, created = Product.objects.get_or_create(
                product_model=product_model,
                defaults={
                    "product_name": row[4],
                    "image_path": IMAGE_PATH,
                    "product_type":product_path.split("\\")[1],
                    "brand":product_path.split("\\")[2],
                    "original_price": original_price,
                    "discount_price": discount_price,
                    "positive_percentage": positive_percentage,
                    "negative_percentage": negative_percentage,
                    "specifications": specifications_json
                }
            )

            # If the product already exists and you want to update its values, you can do so here.
            if not created:
                product.product_name = row[4]
                product.image_path = IMAGE_PATH
                product.original_price = original_price
                product.discount_price = discount_price
                product.positive_percentage = positive_percentage
                product.negative_percentage = negative_percentage
                product.specifications = specifications_json
                product.save()

            print(f'Populating database {i}/{total_rows}')
            i += 1

        except Exception as e:
            print(f"Error processing product on row {i}: {e}")
            i += 1

print(f"Processed {i-1} products out of {total_rows}.")
