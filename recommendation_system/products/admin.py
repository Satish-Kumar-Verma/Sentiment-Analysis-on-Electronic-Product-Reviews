from django.contrib import admin
from .models import Product
from .models import Contact
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_model', 'original_price', 'discount_price', 'positive_percentage', 'status', 'is_featured')  # fields you want to display in list view
    search_fields = ('product_model', 'product_name', 'brand', 'product_type')  # fields you want to search by
    list_editable = ('status', 'is_featured')

admin.site.register(Product, ProductAdmin)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'timestamp']  # fields you want to display in the admin list view
    search_fields = ['name', 'email']  # fields by which you want to allow searching
    list_filter = ['timestamp']  # fields by which you want to allow filtering
