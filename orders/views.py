
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Address, Order
from .serializers import AddressSerializer, OrderSerializer, OrderItemSubmissionSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view




class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)


class PlaceOrderAPIView(APIView):
    def post(self, request, format=None):
        order_serializer = OrderSerializer(data=request.data)
       
        try:
            if order_serializer.is_valid():
                order = order_serializer.save()

                # Save ordered items for the order
                items_data = request.data.get('items', [])
                for item_data in items_data:
                    item_data['order'] = order.id
                    item_serializer = OrderItemSubmissionSerializer(data=item_data)
                    if item_serializer.is_valid():
                        item_serializer.save()
                    else:
                        order.delete()  # Rollback if item validation fails
                        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            print(order_serializer.errors)
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



"""---------Address views ---------"""
@api_view(['GET'])
def get_addresses_by_username(request, username):
    try:
        user = User.objects.get(username=username)
        addresses = Address.objects.filter(user=user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_address(request):
    serializer = AddressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_address(request, pk):
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AddressSerializer(address, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_address(request, pk):
    try:
        address = Address.objects.get(pk=pk)
        
    except Address.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    address.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)