from django.utils.deprecation import MiddlewareMixin

class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            # Người dùng đã đăng nhập, đặt request.custom_info thành số 1
            request.custom_info = 1
        else:
            request.custom_info = 0
