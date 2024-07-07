from django.urls import path
from . import views

urlpatterns = [
    # Get order history by username
    path('order-history/<str:username>/', views.OrderHistoryView.as_view(), name='order-history'),

    # Place order 
    path('place-order/', views.PlaceOrderAPIView.as_view(), name='place_order'),

    #address api endpoint
    path('get-address/<str:username>/', views.get_addresses_by_username),
    path('add-address/', views.add_address),
    path('edit-address/<int:pk>/', views.edit_address),
    path('delete-address/<int:pk>/', views.delete_address),

    

]