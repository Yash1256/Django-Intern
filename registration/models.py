from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from .manager import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Author Email", unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    objects = UserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_superuser and self.is_staff

    def has_perms(self, perm_list, obj=None):
        return self.is_superuser and self.is_staff

    def has_module_perms(self, module):
        return self.is_superuser and self.is_staff


class Author(models.Model):
    email = models.EmailField(verbose_name="Author Email", unique=True, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    added = models.DateTimeField(auto_now_add=True, null=True)
    birthdate = models.DateField(null=False)

    def get_user(self):
        return User.objects.get(email=self.email)

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        db_table = "authors"

    def __str__(self):
        return f"{self.name}({self.email})"
