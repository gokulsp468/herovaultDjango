from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Store
from .serializers import StoreSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from drf_yasg import openapi



class StoreListView(APIView):
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
            store = Store.objects.all()

            if search_term:
                store = store.filter(name__icontains=search_term)

            if from_date:
                store = store.filter(createdAt__gte=from_date)

            if to_date:
                store = store.filter(createdAt__lte=to_date)
            
            if sort_order == 1:
                store = store.order_by(sort_by)
                
            else:
                store = store.order_by(f"-{sort_by}")
           
            # Paginate results
            paginator = Paginator(store, page_limit)
            store_page = paginator.page(page)

            # Serialize paginated categories
            serializer = StoreSerializer(store_page, many=True)
            
            response_data = {
                'data': serializer.data,
                'message': 'store retrieved successfully',
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
    request_body=StoreSerializer, 
    operation_description="Create a new store",
    )
    def post(self, request, format=None):
        serializer = StoreSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'data': serializer.data,
                'message': 'store created successfully'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({'error_message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class StoreDetailView(APIView):
    def get_object(self, pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
         
        store = self.get_object(pk)
        if store == None:
            return Response({"error_message":"store not found"},status=status.HTTP_400_BAD_REQUEST)
        serializer = StoreSerializer(store)
        response_data = {
            'data':serializer.data,
            'message':f'store retrieved successfully'
        }
        return Response(response_data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=StoreSerializer,
        operation_description="edit store"
    )
    def patch(self, request, pk, format=None):
        store = self.get_object(pk)
        if store == None:
            return Response({"error_message":"Category not found"},status=status.HTTP_400_BAD_REQUEST)
        serializer = StoreSerializer(store, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            'data':serializer.data,
            'message':f'edit successfully'
            }
            return Response(response_data,status=status.HTTP_200_OK)
        return Response({'error_message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        store = self.get_object(pk)
        if store == None:
            return Response({"error_message":"Category not found"},status=status.HTTP_400_BAD_REQUEST)
        store.delete()
        return Response({'message':f'{store.name} deleted successfully'},status=status.HTTP_200_OK)