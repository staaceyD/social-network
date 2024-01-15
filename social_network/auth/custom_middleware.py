from social_network.auth.models import UserLastRequest


class LastActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Update last activity
        user = request.user
        if user.is_authenticated:
            last_request = UserLastRequest.objects.get_or_create(user=user)[0]
            last_request.save()

        return response
