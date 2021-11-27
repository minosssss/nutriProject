import hashlib

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager, User, PermissionsMixin
from django.db.models import Q

class Standard(models.Model):
    """ Custom User Model """

    GENDER_MALE = 1
    GENDER_FEMALE = 2

    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
    )

    AGE_1929 = 1929
    AGE_3049 = 3049
    AGE_5064 = 5064

    AGE_CHOICES = (
        (AGE_1929, '19~29'),
        (AGE_3049, '30~49'),
        (AGE_5064, '50~64'),
    )
    n_code = models.CharField(max_length=50, unique=True)
    age_category = models.IntegerField(choices=AGE_CHOICES)
    carb = models.FloatField(blank=True)
    prot = models.FloatField(blank=True)
    fat = models.FloatField(blank=True)
    sodium = models.FloatField(blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)

    class Meta:
        db_table = 'nutri_standard'

    def __str__(self):
        return f'{self.n_code}'


# class UserManager(BaseUserManager):
#     use_in_migrations = True
#
#     def _create_user(self, user_id, password, **extra_fields):
#         if not user_id:
#             raise ValueError('The given user_id must be set')
#
#         user_id = self.user_id
#         user = self.model(user_id=user_id, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, user_id, password=None, **extra_fields):
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(user_id, password, **extra_fields)
#
#     def create_superuser(self, user_id, password, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self._create_user(user_id, password, **extra_fields)


# class UserManager(BaseUserManager):
#     use_in_migrations = True
#
#     def create_user(self, user_id, password, height, weight, **extra_fields):
#         if not user_id:
#             raise ValueError('Users must have an ID')
#
#         user = self.model(
#             user_id=user_id,
#             password=password,
#             height=height,
#             weight=weight,
#         )
#         extra_fields.setdefault('is_superuser', False)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, user_id, password, height, weight, **extra_fields):
#         user = self.create_user(
#             user_id=user_id,
#             password=password,
#             height=height,
#             weight=weight,
#             **extra_fields,
#         )
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user

class UserManager(BaseUserManager):
    def create_user(self, user_id, name, password=None):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not user_id:
            raise ValueError(_('Users must have an user_id address'))

        user = self.model(
            user_id=user_id,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, name, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다.
        """
        user = self.create_user(
            user_id=user_id,
            password=password,
            name=name,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """ Custom User Model """

    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
    )

    AGE_1929 = 1929
    AGE_3049 = 3049
    AGE_5064 = 5064

    AGE_CHOICES = (
        (AGE_1929, '19~29'),
        (AGE_3049, '30~49'),
        (AGE_5064, '50~64'),
    )

    ACTIVITY_1 = 1.2
    ACTIVITY_2 = 1.375
    ACTIVITY_3 = 1.55
    ACTIVITY_4 = 1.725
    ACTIVITY_5 = 1.9
    ACTIVITY_CHOISES = (
        (ACTIVITY_1, '거의 없음'),
        (ACTIVITY_2, '활동량 조금있다.(주1~2회 운동)'),
        (ACTIVITY_3, '활동량 많다.(주3~5회 운동)'),
        (ACTIVITY_4, '활동량 꽤 많다.(주6~7회 운동)'),
        (ACTIVITY_5, '활동량 아주 많다.(매일 2번 운동)'),
    )

    user_id = models.CharField(max_length=20, unique=True, null=False)
    n_code = models.ForeignKey('Standard', on_delete=models.CASCADE, blank=True, null=True, db_column='n_code')
    name = models.CharField(max_length=50)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    age_category = models.IntegerField(choices=AGE_CHOICES, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True)
    activity = models.FloatField(choices=ACTIVITY_CHOISES, null=True)
    proper_cal = models.FloatField(blank=True, null=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    REQUIRED_FIELDS = ['name',]
    USERNAME_FIELD = 'user_id'



    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return f'{self.user_id, self.name, self.n_code, self.proper_cal}'

    class Meta:
        db_table = 'users'

# class Upload(models.Model):
#
#     BREAKFAST = '아침'
#     LUNCH = '점심'
#     DINNER = '저녁'
#
#     MEALTIME_CHOICE = (
#         (BREAKFAST, '아침'),
#         (LUNCH, '점심'),
#         (DINNER, '저녁'),
#     )
#     user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='upload_user', null=False, db_column='user_id')
#     n_code = models.ForeignKey('User', on_delete=models.CASCADE, related_name='upload_code', blank=True, null=True)
#     image = models.ImageField(upload_to=f'%Y/%m/{user}/', null=False)
#     created_at = models.DateField(auto_now_add=True, null=True)
#     mealtimes = models.FloatField(choices=MEALTIME_CHOICE, null=False)
#
#     def __str__(self):
#         return f'{self.user, self.created_at, self.mealtimes}'
#
#     class Meta:
#         db_table = 'user_upload_info'
    # def save(self, *args, **kwargs):
    #     gender = self.gender
    #     code = Standard.objects.get(gender=gender)
    #     self.n_code = code.n_code
    #     # if codename:
    #     #     self.codename = codename
    #     super().save(*args, **kwargs)

    # def save2(self, *args, **kwargs):
    #     height = self.height
    #     weight = self.weight
    #     self.proper_cal = 66.47+(13.75*weight)+(5*height)-(6.76*30)
    #     super().save(*args,**kwargs)

    class Meta:
        db_table = 'users'




