from django.db import models

# Create your models here.

class Product(models.Model):
    product_model = models.CharField(max_length=255, unique=True)
    product_name = models.CharField(max_length=255)
    image_path = models.CharField(max_length=512)
    product_type = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    positive_percentage = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    negative_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    specifications = models.JSONField()
    status = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
