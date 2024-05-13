from functools import wraps
from rest_framework.response import Response

def validate_required_fields(required_fields):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            data = request.data
            for field in required_fields:
                if field not in data or not data[field]:
                    return Response({'error_message': f'Required field "{field}" is missing or empty.'}, status=400)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
