from django.shortcuts import render, get_object_or_404, redirect
from .forms import ContactForm
from .forms import DataExtractionForm
from django.contrib import messages
from .extract_data import * 
from django.db.models import Q
import json

from products.models import Product


def home_page(requests):
    data = Product.objects.filter(is_featured=True).order_by('-positive_percentage')
    return render(requests, 'home.html', {'data': data})


def product_page(request):
    # Start with all products
    products = Product.objects.all()
    
    # If a search query is present, filter products based on the query
    query = request.GET.get('search')
    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(brand__icontains=query) |
            Q(product_type__icontains=query)
        )

    # Fetch distinct product types and brands
    product_types = products.values_list('product_type', flat=True).distinct()
    brands = products.values_list('brand', flat=True).distinct()

    context = {
        'products': products,
        'product_types': product_types,
        'brands': brands
    }
    
    return render(request, 'products.html', context)

def sentiment_analysis_page(request):
    # Get all distinct product types
    product_types = Product.objects.values_list('product_type', flat=True).distinct()

    # This dictionary will contain the data required for our bar charts
    data = {}

    for product_type in product_types:
        # Get all distinct brands for the given product type
        brands = Product.objects.filter(product_type=product_type).values_list('brand', flat=True).distinct()

        # Initialize an empty dictionary to hold brand data for the current product type
        brand_data = {}

        for brand in brands:
            # Get all products of a particular brand and product type
            brand_products = Product.objects.filter(product_type=product_type, brand=brand)

            # Calculate the average positive percentage for the brand
            brand_positive_percentage = sum([product.positive_percentage for product in brand_products]) / len(brand_products)

            # Store the calculated percentages in the brand_data dictionary
            brand_data[brand] = {
                'positive': round(brand_positive_percentage, 2),
                'negative': round(100 - brand_positive_percentage, 2)
            }

        # Assign the brand_data dictionary to the current product type in the main data dictionary
        data[product_type] = brand_data

    context = {
        'data': data
    }
    return render(request, 'sentiment_analysis.html', context)

def about_us(requests):
    return render(requests, 'about_us.html', {})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Redirect to the same page with a success message
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
    
def search_products(requests):
    return render(requests, 'home.html', {})

def display_products(requests):
    products = Product.objects.all()  # Retrieves all products from the database
    return render(requests, 'display_products.html', {'products': products})

def product_details(requests, product_model):
    product = get_object_or_404(Product, product_model=product_model)
    if isinstance(product.specifications, str):
        product.specifications = json.loads(product.specifications)
    return render(requests, 'product_details.html', {'product': product})

def extract_data_view(requests):
    if requests.method == "POST":
        form = DataExtractionForm(requests.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            reviews_link = form.cleaned_data['reviews_link']
            num_pages = form.cleaned_data['num_pages']
            spec_link = form.cleaned_data['spec_link']
            product_type = form.cleaned_data['product_type']
            product_brand = form.cleaned_data['product_brand']
            product_model = form.cleaned_data['product_model']


            reviews_links = [reviews_link + f'{num}' for num in range(1, num_pages + 1)]
        
        reviews = extract_reviews(reviews_links, headers, num_pages)
        image_link = extract_image_link(spec_link, headers)
        specifications = extract_specification(spec_link, headers)

        # Logging the data and saving the extracted information
        try:
            log_data(reviews, specifications, f"{product_type}/{product_brand}/{product_model}", image_link)
            messages.success(requests, 'Data extraction completed successfully!')
            return redirect('extract_data_view')
        except Exception as e:
            messages.error(requests, f'An error occurred: {e}')
    else:
        form = DataExtractionForm()
    return render(requests, 'extract_data.html', {'form': form})


def filtered_products(request):
    # Retrieve a list of all unique brands from your products
    brands = Product.objects.values_list('brand', flat=True).distinct()

    # Get the selected brand(s) from the request
    selected_brands = request.GET.getlist('brand')

    # Get the selected product_type from the request
    product_type = request.GET.get('product_type')

    # Get the selected positive_percentage from the request
    positive_percentage = request.GET.get('positive_percentage')

    # Create a filter dictionary to filter products based on brand, product_type, and positive_percentage
    filters = {}

    if selected_brands:
        filters['brand__in'] = selected_brands

    if product_type:
        filters['product_type'] = product_type

    if positive_percentage:
        # Depending on the selected option, apply the appropriate filter
        if positive_percentage == '90':
            filters['positive_percentage__gt'] = 90
        elif positive_percentage == '80':
            filters['positive_percentage__gt'] = 80
        elif positive_percentage == '50':
            filters['positive_percentage__gt'] = 50
        elif positive_percentage == 'below_50':
            filters['positive_percentage__lt'] = 50  # Filter for positive_percentage below 50

    # Filter products based on selected brands, product_type, and positive_percentage
    filtered_products = Product.objects.filter(**filters)

    # Order the filtered_products by positive_percentage in descending order
    filtered_products = filtered_products.order_by('-positive_percentage')

    # Render the filtered products in a template along with the list of brands
    return render(request, 'filtered_products.html', {'products': filtered_products, 'brands': brands})
