from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        upload_to="categories/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name



class Occasion(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        upload_to="occassions/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class RecipientType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        upload_to="recipients/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    # relations to other model
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categories")
    occasions = models.ManyToManyField(Occasion, blank=True)
    recipient_types = models.ManyToManyField(RecipientType, blank=True)

    # product information
    name = models.CharField(max_length=400, unique=True)
    slug = models.CharField(max_length=400, unique=True)
    description = models.TextField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField()
    featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    # images
    product_image = models.ImageField(
        upload_to='product_images/', blank=True, null=True)
    
    # date and time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
    def average_rating(self):
        average = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return average if average is not None else 0


class Review(models.Model):
    RATINGS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=250, null=True)
    rating = models.IntegerField(choices=RATINGS)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.product.name
