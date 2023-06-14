from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import secrets
import string
# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

class AssetType(models.Model):
    asset_type = models.CharField(max_length=200, unique=True)
    asset_description = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asset_type


class AssetImage(models.Model):
    asset = models.ForeignKey(to="Asset",on_delete=models.CASCADE,null=True,blank=True,related_name="images",   )
    image = models.ImageField(upload_to="media/asset_images/")

    def __str__(self):
        return f"Asset Image: {self.image}"

# models for asset
class Asset(models.Model):
    asset_name = models.CharField(max_length=200)
    asset_code = models.CharField(max_length=200, unique=True, null=True)
    asset_type = models.ForeignKey(to=AssetType, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.asset_code:
            self.asset_code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        # string module is used to generate string of all ascii or digits
        # secret is used to cryptographiclly strong random numbers or given inputs
        characters = string.ascii_letters + string.digits
        unique_code = "".join(secrets.choice(characters) for _ in range(16))
        while Asset.objects.filter(asset_code=unique_code).exists():
            unique_code = "".join(secrets.choice(characters) for _ in range(16))
        return unique_code

    def __str__(self):
        return self.asset_name
