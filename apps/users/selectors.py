from typing import Optional

from django.contrib.auth import get_user_model
from .models import AuthIdentity, AuthProvider

User = get_user_model()


def get_user_by_email(email: str) -> Optional[User]:
    """
    Returns user by email or None.
    """

    return (
        User.objects
        .filter(email=email)
        .first()
    )


def get_email_identity(
    *,
    email: str,
) -> Optional[AuthIdentity]:
    """
    Returns EMAIL auth identity with user joined.
    """

    return (
        AuthIdentity.objects
        .select_related('user')
        .filter(
            provider=AuthProvider.EMAIL,
            provider_user_id=email,
        )
        .first()
    )
