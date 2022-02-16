from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from validate_email import validate_email
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token


class Todo(models.Model):
        user_id = models.IntegerField()
        title = models.TextField()
        description = models.TextField()
        due_date = models.DateField()
        priority = models.TextField()
        is_completed = models.BooleanField(default=False)
        class Meta:
            db_table = "Todo"            
       

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name,confirm_password, password=None):

        if not email:
            raise ValueError("User must have an email")

        if validate_email(email) == False:
            raise ValueError("User must have correct email")

        if CustomUser.objects.filter(email=email).count() > 0:
            raise ValueError("User must have an unique email")

        if not password:
            raise ValueError("User must have a password")

        if confirm_password != password:
            raise ValueError("Password mismatch.")    

        if not first_name:
            raise ValueError("User must have a first name")

        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.set_password(password)  # change password to hash
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    first_name = models.TextField(unique=False)
    last_name = models.TextField(unique=False)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(default=False, max_length=200)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        db_table = "Users"

    def Login(email, password):
        if validate_email(email) == False:
            raise ValueError("User must have correct email")
        if not password:
            raise ValueError("User must have a password")
        output = authenticate(username=email, password=password)
        if output is not None:
            token,_ = Token.objects.get_or_create(user=output)
            return {'error': False, 'auth_token': token.key, 'data': output.asjson(), 'message': "Login Successfully"}
        else:
            return {'error': True, 'auth_token': {}, 'data': {}, 'message': "User Does not Exit."}

    def asjson(self):
        return dict(id=self.id, email=self.email, first_name=self.first_name, last_name=self.last_name)

    def __str__(self):
        return self.email




    