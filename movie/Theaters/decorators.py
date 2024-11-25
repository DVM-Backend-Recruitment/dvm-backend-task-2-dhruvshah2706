from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import Theater, Screen

def theater_admin_required(view_func):
    def _wrapped_view(request,  *args,  **kwargs):
        theater = get_object_or_404(Theater,  pk=kwargs.get('pk'))
        if theater.admin == request.user:
            return view_func(request,  *args,  **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view


def is_theater_admin(view_func):
    def _wrapped_view(request,  *args,  **kwargs):
        screen = get_object_or_404(Screen,  id=kwargs['screen_id'])
        if screen.theater.admin != request.user:
            return HttpResponseForbidden('You do not have permission to edit this screen.')
        return view_func(request,  *args,  **kwargs)
    return _wrapped_view
