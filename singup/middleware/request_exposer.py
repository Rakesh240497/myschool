# from singup.models import thread_local
# class RequestExposerMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         thread_local.request = request
#         response = self.get_response(request)
#         return response
