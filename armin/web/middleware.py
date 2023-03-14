import ipaddress
from .models import Ipaddress
class IpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        try:
            ip_address = Ipaddress.objects.get(ipaddress = ip)
        except Ipaddress.DoesNotExist:
            ip_address = Ipaddress(ipaddress = ip)
            ip_address.save()
        request.user.ip_address = ip_address
        
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response