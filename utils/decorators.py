from products.models import Product
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

def handle_exceptions(handler_func):
    def wrapper(*args, **kwargs):
        try:
            return handler_func(*args, **kwargs)
        except (Product.DoesNotExist, NotFound) as e:
            print(type(e))
            return Response({'message': str(e)}, status=404)
        except PermissionDenied as e:
            print(e)
            return Response({'message': str(e)}, status=403)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
            return Response('An unknown error occurred', status=500)
    return wrapper
