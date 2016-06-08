from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from mail_templated import send_mail


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, email and password.
        """
        if not email:raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Extends the default User profiles of Django. The fields of this model can be obtained by the
    user.get_profile method and it's extended by the django-profile application.
    """
    aums_id = models.CharField(_('Aums ID'),  max_length=32, blank=False, primary_key=True)
    first_name = models.CharField(_('First Name'), max_length=32, blank=True, null=True,
                                  validators=[RegexValidator(regex='^[A-Za-z]*$')])
    last_name = models.CharField(_('Last Name'), max_length=32, blank=True, null=True,
                                    validators=[RegexValidator(regex='^[A-Za-z]*$')])
    email = models.EmailField(_('Email'), db_index=True, unique=True)
    username = models.CharField(_('username'), max_length=32, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_cir_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def __unicode__(self):
        return self.email


class StudentManager(models.Manager):

    def create_student_fromfile(self, aums_id, name, curr_course, branch, tenth_mark, twelth_mark,
                                s1, s2, s3, s4, s5, s6, cgpa, curr_arrears, hist_arrears):
        student = self.create(aums_id=aums_id, name=name, curr_course=curr_course ,branch=branch,
                              tenth_mark=tenth_mark, twelth_mark=twelth_mark, s1=s1, s2=s2, s3=s3, s4=s4,
                              s5=s5, s6=s6, cgpa=cgpa, curr_arrears=curr_arrears, hist_arrears=hist_arrears)

        # do something with the book
        return student


class Student(models.Model):
    stud_id = models.AutoField(primary_key=True)
    aums_id = models.CharField(_('Aums ID'),  max_length=32, blank=False, unique=True)
    name = models.CharField(_('First Name'), max_length=32, blank=True, null=True)
    curr_course = models.CharField(_('Current Course'), max_length=32, blank=True, null=True,
                                  validators=[RegexValidator(regex='^[A-Za-z]*$')])
    branch = models.CharField(_('Branch'), max_length=32, blank=True, null=True,
                                  validators=[RegexValidator(regex='^[A-Za-z]*$')])
    tenth_mark = models.CharField(_('10th Mark'),max_length=5, blank=True, null=True)
    twelth_mark = models.CharField(_('12th Mark'),max_length=5, blank=True, null=True)
    s1 = models.CharField(_('S1 Mark'), max_length=5, blank=True, null=True)
    s2 = models.CharField(_('S2 Mark'), max_length=5, blank=True, null=True)
    s3 = models.CharField(_('S3 Mark'), max_length=5, blank=True, null=True)
    s4 = models.CharField(_('S4 Mark'), max_length=5, blank=True, null=True)
    s5 = models.CharField(_('S5 Mark'), max_length=5, blank=True, null=True)
    s6 = models.CharField(_('S6 Mark'), max_length=5, blank=True, null=True)
    cgpa = models.CharField(_('CGPA'), max_length=5,blank=True, null=True)
    curr_arrears = models.CharField(_('No of current arrears'),max_length=5, blank=True, null=True)
    hist_arrears = models.CharField(_('No of history arrears'),max_length=5, blank=True, null=True)

    Objects = StudentManager()