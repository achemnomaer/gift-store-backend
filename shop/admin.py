from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

from .models import (Category, Occasion, Product, RecipientType, Review)


# registering category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_image', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        # Add a default image URL here if needed
        return format_html('<img src="http://127.0.0.1:8000/static/images/no-image.jpg" width="50" height="50" />')

    display_image.short_description = 'Image'



# registering occassion model
@admin.register(Occasion)
class OccassionAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_image', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        # Add a default image URL here if needed
        return format_html('<img src="http://127.0.0.1:8000/static/images/no-image.jpg" width="50" height="50" />')

    display_image.short_description = 'Image'


# registering recipient type model
@admin.register(RecipientType)
class RecipientTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_image', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        # Add a default image URL here if needed
        return format_html('<img src="http://127.0.0.1:8000/static/images/no-image.jpg" width="50" height="50" />')

    display_image.short_description = 'Image'



# registering product model
@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'details')
    list_display = ['name', 'display_image', 'price', 'discounted_price',
                    'stock_quantity', 'featured', 'created_at', 'updated_at']
    list_filter = ['featured', 'created_at', 'updated_at']
    list_editable = ['price', 'discounted_price', 'stock_quantity', 'featured']
    prepopulated_fields = {'slug': ('name',)}

    def display_image(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" width="60" height="60" />'.format(obj.product_image.url))
        # Add a default image URL here if needed
        return format_html('<img src="http://127.0.0.1:8000/static/images/no-image.jpg" width="60" height="60" />')

    display_image.short_description = 'Image'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ["id", "name", "rating", "created_at"]
    list_filter = ['rating', 'created_at',]
