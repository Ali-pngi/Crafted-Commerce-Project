from products.models import Product
from offers.models import Offer
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

# Decorator function that handles all handler method exceptions
def handle_exceptions(handler_func):
    def wrapper(*args, **kwargs):
        try:
            return handler_func(*args, **kwargs)
        except (Product.DoesNotExist, Offer.DoesNotExist, NotFound) as e:
            print(type(e))
            return Response({ 'message': str(e) }, 404)
        except PermissionDenied as e:
            print(e)
            return Response({ 'message': str(e) }, 403)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
            return Response('An unknown error occurred', 500)
    return wrapper