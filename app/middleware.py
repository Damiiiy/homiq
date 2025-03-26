from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in [reverse('login-c'), reverse('register')]:
            request.session['next'] = request.get_full_path()
            return redirect('login-c')
        return self.get_response(request)
