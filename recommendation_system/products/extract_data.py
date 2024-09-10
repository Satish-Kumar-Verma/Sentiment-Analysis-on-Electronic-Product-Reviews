from bs4 import BeautifulSoup
import requests
import re
import pickle
import os
from datetime import datetime

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

def add_product_to_mappings(product_title, file_path):
    # Check if the file exists
    if os.path.isfile('dir_mappings.pkl'):
        # Load the dictionary from the file
        with open('dir_mappings.pkl', 'rb') as file:
            data = pickle.load(file)
    else:
        # Create a new dictionary
        data = {
            "product_titles": [],
            "product_paths": []
        }

    # Retrieve the existing product_titles and product_paths
    product_titles = data['product_titles']
    product_paths = data['product_paths']

    # Check if the new_path already exists in the dictionary
    if file_path not in product_paths:
        # Add the new item to the dictionary
        product_titles.append(product_title)
        product_paths.append(file_path)

        # Update the dictionary
        data['product_titles'] = product_titles
        data['product_paths'] = product_paths

        # Write the updated dictionary back to the file
        with open('dir_mappings.pkl', 'wb') as file:
            pickle.dump(data, file)
        return True
    else:
        return False


def log_data(review_data, specification_data, filepath, image_link):
    try:
        if add_product_to_mappings(specification_data[0], filepath):
            os.makedirs(filepath, exist_ok=True)  # Create directory if it doesn't exist

            with open(os.path.join(filepath, "reviews.bin"), 'wb') as file:
                pickle.dump(review_data, file)

            with open(os.path.join(filepath, "specifications.bin"), 'wb') as file:
                pickle.dump(specification_data, file)

            image_data = requests.get(image_link).content
            with open(os.path.join(filepath, "image.jpeg"), 'wb') as file:
                file.write(image_data)

            with open('write_logs.txt', 'a') as file:
                file.write(
                    f'{datetime.now().strftime("%d.%m.%Y %I:%M:%S %p")} : {specification_data[0]} : {filepath}\n')

            print(f"Product Name: {specification_data[0]}")
            print('Reviews, specifications, image, and price are successfully stored.')
            print('Item is added successfully to the dir_mappings file.')
        else:
            print("Duplicate filepath found. Item not added.")

    except Exception as e:
        print(f"An error occurred while storing the data: {e}")


def extract_reviews(reviews_links, headers, num_pages):

    """This function returns the reviews extracted from the given link in the form of list of lists.
    list[list1] - list1 : [review, review time]
    """
    print("[+] Extracting reviews...")

    review_data = []

    i = 1

    for rv_link in reviews_links:
        response = requests.get(rv_link, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        reviews_div = soup.find('div', class_="_1YokD2 _3Mn1Gg col-9-12")

        reviews_containers = reviews_div.find_all('div', class_="_27M-vq")

        for review in reviews_containers:
            rv_data = review.find('div', class_="t-ZTKy")
            rv_time = review.find('div', class_='row _3n8db9')
            if rv_data:
                rv_data = rv_data.text.strip()
            if rv_time:
                rv_time = rv_time.text.strip()
                pattern = r"(\d+ (?:month|day)s? (?:and )?)+ago"

                match = re.search(pattern, rv_time)
                if match:
                    rv_time = match.group(0)
                else:
                    rv_time = ""
                review_data.append([rv_data, rv_time])
        print(f'[+] Reviews extracted form page {i}/{num_pages}.')
        i += 1
    print("Done!")
    return review_data


def extract_specification(spec_link, headers):
    """This function returns the product specifications extracted from the given link in the form of a list of lists.
    The first element is the product name (str), and the second element is a dictionary of specifications.
    """
    print("[+] Extracting specifications...", end='')

    response = requests.get(spec_link, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    product_title = soup.find('span', class_='B_NuCI').text.strip()

    # print(product_title)

    specification_data = soup.find('div', class_="_3dtsli")

    specification_div = specification_data.find('div', '_1UhVsV')

    specifications = {}

    tables = specification_div.find_all('table', class_='_14cfVK')

    for table in tables:
        category = table.previous_sibling.text.strip()

        specifications[category] = {}

        rows = table.find_all('tr', class_='_1s_Smc row')

        for row in rows:
            key = row.find('td', class_="_1hKmbr col col-3-12").text.strip()
            value = row.find('td', class_="URwL2w col col-9-12").text.strip()

            specifications[category][key] = value

    price_discount = soup.find('div', class_='_30jeq3 _16Jk6d')

    price_discount = price_discount.text.strip() if price_discount else "Price not available"

    price_original = soup.find('div', class_='_3I9_wc _2p6lqe')
    price_original = price_original.text.strip() if price_original else "Price not available"
    specifications["Price"] = {"Discount": price_discount, "Original": price_original}

    print('Done!')
    return [product_title, specifications]


def extract_image_link(spec_link, headers):
    """This function extracts the image link from the given specifications link."""
    response = requests.get(spec_link, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    image_link = soup.select_one('img._396cs4')['src']
    return image_link


def main():

    reviews_link = input("Enter the reviews link: ")
    num_pages = int(input("No. of pages: "))
    reviews_links = [reviews_link + f'{num}' for num in range(1, num_pages + 1)]

    spec_link = input("Enter the specifications link: ")

    reviews = extract_reviews(reviews_links, headers, num_pages)

    for review in reviews:
        print(review)

    image_link = extract_image_link(spec_link, headers)

    specifications = extract_specification(spec_link, headers)

    for category, details in specifications[1].items():
        print(f"{category}")
        for key, val in details.items():
            print(f"{key} : {val}")
        print()

    product_type = input("Product Type: ")
    product_brand = input("Product Brand: ")
    product_model = input("Product Model: ")

    log_data(reviews, specifications, f"{product_type}/{product_brand}/{product_model}", image_link)


if __name__ == '__main__':
    main()
