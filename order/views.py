from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from order import serializers as orderSz
from order.serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer
from order.models import Cart, CartItem, Order
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from product.permissions import IsReviewAuthorOrReadonly
from rest_framework.decorators import action
from order.services import OrderService
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # return Cart.objects.filter(user=self.request.user)
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        existing_cart = Cart.objects.filter(user=request.user).first()

        if existing_cart:
            serializer = self.get_serializer(existing_cart)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return super().create(request, *args, **kwargs)




class CartItemViewSet(ModelViewSet):
    # queryset = CartItem.objects.all()
    # serializer_class = CartItemSerializer

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context

        # return {'cart_id': self.kwargs['cart_pk']}
        return {'cart_id': self.kwargs.get('cart_pk')}

    def get_queryset(self):
        # return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
        # return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs.get('cart_pk'))



class OrderViewset(ModelViewSet):
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # permission_classes = [IsReviewAuthorOrReadonly]

    

    http_method_names = ['get', 'post', 'delete', 'patch', 'head', 'options']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user=request.user)
        return Response({'status': 'Order canceled'})

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = orderSz.UpdateOrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f"Order status updated to {request.data['status']}"})

    # def get_permissions(self):
    #     # if self.request.method in ['PATCH', 'DELETE']:
    #     if self.request.method == 'DELETE':
    #         return [IsAdminUser()]
    #     return [IsAuthenticated()]
    

    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    

    # def get_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return CreateOrderSerializer
    #     return OrderSerializer

    # def get_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return CreateOrderSerializer
    #     if self.request.method == 'PATCH':
    #         return UpdateOrderSerializer
    #     return OrderSerializer

    def get_serializer_class(self):
        if self.action == 'cancel':
            return orderSz.EmptySerializer
        if self.action == 'create':
            return orderSz.CreateOrderSerializer
        elif self.action == 'update_status':
            return orderSz.UpdateOrderSerializer
        return orderSz.OrderSerializer

    def get_serializer_context(self):
        # return {'user_id': self.request.user.id}
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user': self.request.user}

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        
        if self.request.user.is_staff:
        #     return Order.objects.all()
        # return Order.objects.filter(user=self.request.user)
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)


    