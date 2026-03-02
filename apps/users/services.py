from django.db import transaction, IntegrityError
from django.contrib.auth import get_user_model

from .models import AuthIdentity, AuthProvider
from .selectors import get_user_by_email
from .exceptions import UserAlreadyExistsError


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
