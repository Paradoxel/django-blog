from django.core.exceptions import PermissionDenied
from apps.accounts.models import UserTypes
from django.shortcuts import redirect

class WriterRequiredMixin:
    """
    Restricts access to writer-only users.
    Must be used AFTER LoginRequiredMixin.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.is_writer:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
    


class DeleteAccountVerificationRequiredMixin:

    def dispatch(self, request, *args, **kwargs):

        if not request.session.get("delete_account_verified"):
            return redirect("accounts:delete_account")

        return super().dispatch(request, *args, **kwargs)
    


class ReaderRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.user_type != UserTypes.READER:
            return redirect("accounts:profile")
        return super().dispatch(request, *args, **kwargs)