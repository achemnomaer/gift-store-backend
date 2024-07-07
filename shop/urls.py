from django.urls import path

from . import views

app_name = "shop" 

urlpatterns = [
    # Get all categories
    path('categories/', views.CategoriesView.as_view(), name='categories'),

    # Get all occasions
    path('occasions/', views.OccasionsView.as_view(), name='occasions'),

    # Get all recipients
    path('recipients/', views.RecipientsView.as_view(), name='recipients'),

     # Get all featured products
    path('featured-products/', views.FeaturedProductsView.as_view(), name='featured-products'),

     # Get single product detail
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),

     # Get all the reviews for a single product
    path('reviews/<slug:product_slug>/', views.ProductReviewListView.as_view(), name='product-reviews'),

    # Submit the review
    path('submit-review/<slug:product_slug>/', views.SubmitReviewView.as_view(), name='submit-review'),

    # Searching the product
    path('search/', views.ProductSearchView.as_view(), name='product-search'),

    path('products/', views.ProductListView.as_view(), name='product-list'),

]
