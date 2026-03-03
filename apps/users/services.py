from django.db import transaction, IntegrityError
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AuthIdentity, AuthProvider
from .selectors import get_user_by_email, get_email_identity
from .exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserInactiveError,
)


User = get_user_model()


@transaction.atomic
def register_user(
    *,
    email: str,
    password: str,
) -> User:

    if get_user_by_email(email=email):
        raise UserAlreadyExistsError()

    try:
        user = User(
            email=email,
        )

        user.set_password(password)
        user.save()

        AuthIdentity.objects.create(
            user=user,
            provider=AuthProvider.EMAIL,
            provider_user_id=email,
        )

    except IntegrityError:
        raise UserAlreadyExistsError()

    return user


def login_user(
    *,
    request,
    email: str,
    password: str,
):
    """
    Authenticates user via email identity.
    Creates session and returns JWT tokens.
    """
    identity = get_email_identity(email=email)
    user = identity.user

    if not identity or not check_password(password, user.password):
        raise InvalidCredentialsError()

    if not user.is_active:
        raise UserInactiveError()

    login(request, user)

    refresh = RefreshToken.for_user(user)

    return {
        'user': user,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
