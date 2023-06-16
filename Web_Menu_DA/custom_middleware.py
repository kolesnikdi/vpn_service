from django.urls import reverse

ALLOWED_URL_METHODS_2FA = {
    # reverse('registration_confirm'): ['GET', 'OPTIONS', 'HEAD', 'DELETE', 'POST', 'PUT', 'PATCH', 'DELETE'],
    # reverse('list_menu'): ['GET', 'OPTIONS', 'HEAD', 'DELETE', 'POST', 'PUT', 'PATCH', 'DELETE']
}



class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("custom middleware before next middleware/view")
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each response after the view is called
        #
        print("custom middleware after response or previous middleware")

        return response