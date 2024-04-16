from django.db import models
from django.forms import ValidationError
from django.utils.timezone import now
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser



class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, userType, password=None, confirmPass=None, is_active=True):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,      
            userType=userType,
            is_active=is_active
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, userType, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            userType=userType
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=50)
    typeChoices = [
        ('Admin', 'Admin'),
        ('Project_Manager', 'Project_Manager'),
        ('Team_Leader', 'Team_Leader'),
        ('Employee', 'Employee'),
    ]
    userType = models.CharField(max_length=100, choices=typeChoices) 
    allocation_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)   

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "userType"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Project(models.Model):
    projectCreator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_id = models.AutoField(primary_key=True)
    projectName = models.CharField(max_length=50)
    projectDescription = models.CharField(max_length=500)
    project_assigned_on = models.DateTimeField(default=now().date)
    # brfore doing anyother change i need to remove now().date
    projectStartDate = models.DateField(default=project_assigned_on)
    projectEndDate = models.DateField(null=True)
    toDo = models.CharField(max_length=100, choices=(('In progress', 'In progress'),('Completed', 'Completed')))

    def clean(self):
        if self.projectStartDate < self.project_assigned_on:
            raise ValidationError("Start date cannot be before the project assigned date.")
# this method will not retun any value in the end