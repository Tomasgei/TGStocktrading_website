from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=200, unique=True, blank=True, verbose_name= _("Username"))
    email = models.EmailField(max_length=200, unique=True, blank=False, verbose_name= _("Email adress"))
    first_name = models.CharField(max_length=200, blank=True, verbose_name= _("First name"))
    last_name = models.CharField(max_length=200, blank=True, verbose_name= _("Surname"))
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name=_("User")
        verbose_name_plural=_("Users")
    def __str__(self) -> str:
        return self.username
    
    @property
    def get_full_name(self) -> str:
        return f"{self.first_name.title()} {self.last_name.title()}"
    
    def get_short_name(self) -> str:
        return self.username
    
