from django.db import models

# Create your models here

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items')
    image = models.ImageField(upload_to='static/students', blank=True)
    making_time = models.PositiveIntegerField(help_text='In minutes')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    description = models.TextField(blank=True)
    available_plates = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, registration_number, password, mobile_number=None):
        if not username:
            raise ValueError('Users must have a username')
        if not registration_number:
            raise ValueError('Users must have a registration number')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            username=username,
            registration_number=registration_number,
            mobile_number=mobile_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, registration_number, password, mobile_number=None):
        user = self.create_user(
            username=username,
            registration_number=registration_number,
            password=password,
            mobile_number=mobile_number,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    registration_number = models.CharField(max_length=10, unique=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['registration_number']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem, through='CartItem')

class CartItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)