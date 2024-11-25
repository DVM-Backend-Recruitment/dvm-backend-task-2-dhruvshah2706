from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import Show


def is_theater_admin(view_func):
    def _wrapped_view(request,  *args,  **kwargs):
        show = get_object_or_404(Show,  id=kwargs['show_id'])
        if show.theater.admin != request.user:
            return HttpResponseForbidden('You do not have permission to edit this show.')
        return view_func(request,  *args,  **kwargs)
    return _wrapped_view