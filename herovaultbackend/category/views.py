from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from drf_yasg import openapi



class CategoryListView(APIView):
    def get(self, request, format=None):
        try:
            # Extract query parameters
            page = int(request.query_params.get('page', 1))
            page_limit = int(request.query_params.get('page_limit', 10))
            search_term = request.query_params.get('searchTerm', '')
            sort_by = request.query_params.get('sortBy', 'createdAt')
            sort_order = int(request.query_params.get('sortOrder', -1))
            from_date = request.query_params.get('fromDate', None)
            to_date = request.query_params.get('toDate', None)

            # Parse date strings to date objects
            if from_date:
                from_date = parse_date(from_date)
            if to_date:
                to_date = parse_date(to_date)

            # Apply filters based on query parameters
            categories = Category.objects.all()

            if search_term:
                categories = categories.filter(name__icontains=search_term)

            if from_date:
                categories = categories.filter(createdAt__gte=from_date)

            if to_date:
                categories = categories.filter(createdAt__lte=to_date)
            
            if sort_order == 1:
                categories = categories.order_by(sort_by)
                
            else:
                categories = categories.order_by(f"-{sort_by}")
           
            # Paginate results
            paginator = Paginator(categories, page_limit)
            categories_page = paginator.page(page)

            # Serialize paginated categories
            serializer = CategorySerializer(categories_page, many=True)
            
            response_data = {
                'data': serializer.data,
                'message': 'Categories retrieved successfully',
                'page_info': {
                    'page': page,
                    'page_limit': page_limit,
                    'total_pages': paginator.num_pages,
                    'total_items': paginator.count,
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error_message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        
    @swagger_auto_schema(
    request_body=CategorySerializer, 
    operation_description="Create a new category",
    )
    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'data': serializer.data,
                'message': 'Category created successfully'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({'error_message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetailView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
         
        category = self.get_object(pk)
        if category == None:
            return Response({"error_message":"Category not found"},status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(category)
        response_data = {
            'data':serializer.data,
            'message':f'category retrieved successfully'
        }
        return Response(response_data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=CategorySerializer,
        operation_description="edit category"
    )
    def patch(self, request, pk, format=None):
        category = self.get_object(pk)
        if category == None:
            return Response({"error_message":"Category not found"},status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(category, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            'data':serializer.data,
            'message':f'edit successfully'
            }
            return Response(response_data,status=status.HTTP_200_OK)
        return Response({'error_message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        if category == None:
            return Response({"error_message":"Category not found"},status=status.HTTP_400_BAD_REQUEST)
        category.delete()
        return Response({'message':f'{category.name} deleted successfully'},status=status.HTTP_200_OK)