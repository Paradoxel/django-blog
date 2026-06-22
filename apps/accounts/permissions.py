from django.core.exceptions import PermissionDenied
from apps.accounts.models import UserTypes
from django.shortcuts import redirect

class WriterRequiredMixin:
    """
    Restricts access to writer-only users.
    Must be used AFTER LoginRequiredMixin.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.user_type != UserTypes.WRITER:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)