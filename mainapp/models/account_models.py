from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
import os

class UserManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None):
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True)
    
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    def has_perm(self, prerm, obj=None):
        "Does the user have a specific permission?"
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app 'app_label'?"
        return True
    
    def email_user(self, subject, message):
        email_from = os.environ['EMAIL_HOST_USER']
        email_to = [self.email]
        send_mail(
            subject,
            message,
            email_from,
            email_to,
            fail_silently=False,
        )
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_onetoone(sender, **kwargs):
    if kwargs['created']:
        from mainapp.models.profile_models import Profile
        
        Profile.objects.create(user=kwargs['instance'])
    
