from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category, Review
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from product.paginations import DefaultPagination
# from rest_framework.permissions import IsAdminUser, AllowAny
from api.permissions import IsAdminOrReadOnly, FullDjangoModelPermission
from rest_framework.permissions import DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from product.permissions import IsReviewAuthorOrReadonly



# Create your views here.


# def view_products(request):
#     return HttpResponse("Okay")


# @api_view()
# def view_products(request):
#     return Response({"message":"Okay"})


# @api_view()
# def view_products(request):
#     products = Product.objects.select_related('category').all()
#     serializer = ProductSerializer(products, many=True, context={'request': request})

#     return Response(serializer.data)

@api_view(['GET', 'POST'])
def view_products(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category').all()
        # serializer = ProductSerializer(products, many=True, context={'request': request})
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        # serializer = ProductSerializer(data=request.data) # Deserializer
        # if serializer.is_valid():
        #     print(serializer.validated_data)
        # # serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     # return Response('Okay')
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ViewProducts(APIView):

    def get(self, request):
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



# @api_view()
# def view_specific_product(request, id):
#     product = get_object_or_404(Product, pk=id)
#     product_dict = {'id': product.id, 'name': product.name, 'price': product.price}

#     return Response(product_dict)



# @api_view()
# def view_specific_product(request, id):
#     product = get_object_or_404(Product, pk=id)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def view_specific_product(request, id):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    if request.method == 'PUT':
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method == 'DELETE':
        product = get_object_or_404(Product, pk=id)
        # copy_of_product = product
        product.delete()
        # serializer = ProductSerializer(copy_of_product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ViewSpecificProduct(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ProductList(ListCreateAPIView):
    # queryset = Product.objects.select_related('category').all()
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.select_related('category').all()
    
    # def get_serializer_class(self):
    #     return ProductSerializer
    
    # def get_serializer_context(self):
    #     return {'request': self.request}
    

class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    # def delete(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     if product.stock > 10:
    #         return Response({'message': "Product with stock more than 10 could not be deleted"})
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['category_id', 'price']
    filterset_class = ProductFilter
    # pagination_class = PageNumberPagination
    pagination_class = DefaultPagination
    # search_fields = ['name', 'description', 'category__name']
    search_fields = ['name', 'description']
    # ordering_fields = ['price']
    ordering_fields = ['price', 'updated_at']

    # permission_classes = [IsAdminUser]
    permission_classes = [IsAdminOrReadOnly]

    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [FullDjangoModelPermission]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAdminUser()]
   

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     category_id = self.request.query_params.get('category_id')

    #     if category_id is not None:
    #         queryset = Product.objects.filter(category_id=category_id)
        
    #     return queryset


    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response({'message': "Product with stock more than 10 could not be deleted"})
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)



class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(
        product_count=Count('products')).all()
    serializer_class = CategorySerializer

    

@api_view()
def view_categories(request):
    # categories = Category.objects.all()
    categories = Category.objects.annotate(product_count=Count('products')).all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


class ViewCategories(APIView):
    def get(self, request):
        categories = Category.objects.annotate(product_count=Count('products')).all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view()
def view_specific_category(request, id):
    category = get_object_or_404(Category.objects.annotate(product_count=Count('products')).all(), pk=id)
    serializer = CategorySerializer(category)
    return Response(serializer.data)


class ViewSpecificCategory(APIView):
    def get(self, request, id):
        category = get_object_or_404(Category.objects.annotate(product_count=Count('products')).all(), pk=id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, id):
        category = get_object_or_404(Category.objects.annotate(product_count=Count('products')).all(), pk=id)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        category = get_object_or_404(Category.objects.annotate(product_count=Count('products')).all(), pk=id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(ListCreateAPIView):
    # queryset = Category.objects.select_related('products').all()
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    # def get_queryset(self):
    #     return Category.objects.select_related('products').all()
    
    # def get_serializer_class(self):
    #     return CategorySerializer
    
    # def get_serializer_context(self):
    #     return {'request': self.request}



class CategoryDetails(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer

    # def delete(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     if product.stock > 10:
    #         return Response({'message': "Product with stock more than 10 could not be deleted"})
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)




class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}