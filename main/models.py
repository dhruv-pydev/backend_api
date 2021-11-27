from django.utils.functional import cached_property
from django.db import models
from django.contrib.auth.models import User


class BaseUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="base_user")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.username}"

    @cached_property
    def full_name(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    @cached_property
    def username(self) -> str:
        return f"{self.user.username}"

    @cached_property
    def first_name(self) -> str:
        return f'{self.user.first_name}'

    @cached_property
    def last_name(self) -> str:
        return f'{self.user.last_name}'
