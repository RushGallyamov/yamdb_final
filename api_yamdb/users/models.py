from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    roles = Choices(USER, MODERATOR, ADMIN)

    email = models.EmailField(unique=True)
    role = StatusField(choices_name="roles", default=USER, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    confirmation_code = models.CharField(max_length=10, blank=True)

    def set_confirmation_code(self, data):
        """Устанавливает код_подтверждения у юзера."""
        self.confirmation_code = data
        self.save()

    def remove_confirmation_code(self):
        """Удаляет код_подтверждения у юзера."""
        self.confirmation_code = 0
        self.save()

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator_or_admin(self):
        return self.role == self.MODERATOR or self.is_admin
