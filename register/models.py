from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True, null=True, blank=True)
    profile_image = models.ImageField(upload_to="users/images/", null=True, blank=True)
    groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        related_name="customuser_groups",  # 이렇게 related_name 추가!
        related_query_name="user",
    )


    user_permissions = models.ManyToManyField(
        "auth.Permission",
        blank=True,
        related_name="customuser_permissions",  # 이렇게 related_name 추가!
        related_query_name="user",
    )
