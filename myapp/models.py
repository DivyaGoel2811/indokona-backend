from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

ROLE_CHOICES = [
    ('customer', 'Customer'),
    ('connector', 'Connector Partner'),
    ('retailer', 'Retailer'),
    ('distributor', 'Distributor'),
    ('master_distributor', 'Master Distributor'),
    ('super_distributor', 'Super Distributor'),
    ('franchise', 'Franchise'),
    ('b2b_panel', 'B2B Panel'),
]

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, role, password=None):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, role=role)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, full_name, password):
        user = self.create_user(email, full_name, role='admin', password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']

    def __str__(self):
        return f"{self.email} ({self.role})"
