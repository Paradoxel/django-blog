from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class WriterRequiredMixin:
    """
    Restrict access to writer-only users.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.is_writer:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class DeleteAccountVerificationRequiredMixin:
    """
    Ensure account deletion has been verified.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("delete_account_verified"):
            return redirect("accounts:delete_account")

        return super().dispatch(request, *args, **kwargs)


class ReaderRequiredMixin:
    """
    Restrict access to reader-only users.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.is_writer:
            return redirect("accounts:profile")

        return super().dispatch(request, *args, **kwargs)