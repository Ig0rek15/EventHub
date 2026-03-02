from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models


class UserRole(models.TextChoices):
    USER = 'user', 'User'
    ORGANIZER = 'organizer', 'Organizer'


class UserManager(BaseUserManager):

    def create_user(self, email: str, password: str | None = None, **extra):
        if not email:
            raise ValueError('Email required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class AuthProvider(models.TextChoices):
    EMAIL = 'email', 'Email'
    TELEGRAM = 'telegram', 'Telegram'


class AuthIdentity(models.Model):

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='identities',
    )

    provider = models.CharField(
        max_length=20,
        choices=AuthProvider.choices,
    )

    provider_user_id = models.CharField(
        max_length=255,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            'provider',
            'provider_user_id',
        )
