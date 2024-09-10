from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('products', views.product_page, name='products'),
    path('sentiment_analysis', views.sentiment_analysis_page, name='sentiment_analysis'),
    path('about_us', views.about_us, name='about_us'),
    path('contact', views.contact, name='contact'),
    path('search', views.search_products, name='search'),
    path('display-products/', views.display_products, name='display_products'),
    path('product_details/<str:product_model>/', views.product_details, name='product_details'),
    path('extract-data/', views.extract_data_view, name='extract_data_view'),
    path('filter-products', views.filtered_products, name='filtered_products'),
]
