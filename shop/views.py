from django.db.models import Q
from rest_framework import filters, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Avg
from rest_framework import status


from .models import (Category, Occasion, Product, RecipientType, Review)
from .serializers import (CategorySerializer,
                          OccasionSerializer, ProductSearchSerializer,
                          ProductSerializer, RecipientSerializer,
                          ReviewSerializer, SimpleProductSerializer)



# To get all categories
class CategoriesView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):

        return Category.objects.all()

# To get all occasions 
class OccasionsView(generics.ListAPIView):
    serializer_class = OccasionSerializer

    def get_queryset(self):

        return Occasion.objects.all()

# To get all recipients
class RecipientsView(generics.ListAPIView):
    serializer_class = RecipientSerializer

    def get_queryset(self):

        return RecipientType.objects.all()

# To get featured products
class FeaturedProductsView(generics.ListAPIView):
    serializer_class = SimpleProductSerializer

    def get_queryset(self):

        return Product.objects.filter(featured=True)


# To get single product detail 
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

# To get all reviews for a single product
class ProductReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_slug = self.kwargs['product_slug']
        return Review.objects.filter(product__slug=product_slug)

# To submit a review
class SubmitReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        product_slug = self.kwargs.get('product_slug')
        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            return Response({"error": "Product with the given slug does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        data['product'] = product.id  # Add the product ID to the request data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# To search product based on name and description
class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListView(generics.ListAPIView):
    serializer_class = SimpleProductSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Product.objects.all()

        # Filter based on parameters in the query string
        filters = Q()

        occasion = self.request.query_params.get('occasion')
        if occasion:
            filters &= Q(occasions__slug=occasion)

        recipient_type = self.request.query_params.get('recipient_type')
        if recipient_type:
            filters &= Q(recipient_types__slug=recipient_type)


        category = self.request.query_params.get('category')
        if category:
            filters &= Q(category__slug = category)

        min_price = self.request.query_params.get('min_price')
        if min_price:
            filters &= Q(discounted_price__gte=min_price)

        max_price = self.request.query_params.get('max_price')
        if max_price:
            filters &= Q(discounted_price__lte=max_price)


        # Sorting parameters
        sort_by = self.request.query_params.get('sort_by')
        if sort_by == 'priceLowToHigh':
            queryset = queryset.order_by('discounted_price')
        elif sort_by == 'priceHighToLow':
            queryset = queryset.order_by('-discounted_price')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'ratingLowToHigh':
            queryset = queryset.annotate(avg_rating=Avg('reviews__rating')).order_by('avg_rating')
        elif sort_by == 'ratingHighToLow':
            queryset = queryset.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')

        return queryset.filter(filters)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_count = queryset.count()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data, total_count=total_count)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_paginated_response(self, data, total_count):
        response = super().get_paginated_response(data)
        response.data['total_count'] = total_count
        return response
