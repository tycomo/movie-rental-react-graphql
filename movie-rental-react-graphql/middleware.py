from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class JWTMiddleware:
    def __init__(self, get_response):
            self.get_response = get_response
            # One-time configuration and initialization.

    def __call__(self, request):
            # token = request.META.get('HTTP_AUTHORIZATION', '')
            # if not token.startswith('JWT'):
            #     return
            # jwt_auth = JSONWebTokenAuthentication()
            # auth = None
            # try:
            #     auth = jwt_auth.authenticate(request)
            # except Exception:
            #     return
            # request.user = auth[0]
            return