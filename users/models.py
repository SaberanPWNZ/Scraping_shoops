import logging

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

logger = logging.getLogger('users')


class Role(models.Model):
    role = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role


class CustomUserManager(BaseUserManager):
    """Custom user manager model"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            logger.error("Attempt to create user without email")
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            try:
                validate_password(password)
                user.set_password(password)
            except ValidationError as e:
                logger.exception(f"Invalid password for user {email}")
                raise ValueError(f"Invalid password: {', '.join(e.messages)}")
        else:
            logger.error(f"Attempt to create user {email} without password")
            raise ValueError('Password must be provided')

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a new superuser with the given email and password."""

        if not password:
            logger.error("Password must be provided for superuser creation.")
            raise ValueError("The password must be set.")

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        try:
            user = self.create_user(email, password, **extra_fields)
            logger.info("New superuser created", extra={'email': email})
            return user
        except Exception as e:
            logger.error(f"Failed to create superuser: {e}")
            raise


class User(AbstractBaseUser):
    """User Model"""
    user_phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            ),
        ],
    )
    email = models.EmailField(max_length=100, unique=True, blank=False)
    telegram_id = models.CharField(max_length=50, blank=False, unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"
        ordering = ["first_name", "last_name"]
        unique_together = ("telegram_id", "user_phone")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['telegram_id']

    objects = CustomUserManager()



    def __str__(self):
        """Return a string representation of the user."""
        return self.email