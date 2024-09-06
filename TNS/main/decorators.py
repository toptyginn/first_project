import re
from django.http import HttpResponseForbidden

MOBILE_USER_AGENT_REGEX = re.compile(r"Mobile|Android|iPhone|iPad|iPod", re.IGNORECASE)

def mobile_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        if not MOBILE_USER_AGENT_REGEX.search(user_agent):
            return HttpResponseForbidden("Доступ разрешен только с мобильных устройств")

        return view_func(request, *args, **kwargs)

    return _wrapped_view