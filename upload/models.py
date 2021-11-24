from django.db import models
from accounts.models import User, Standard
from upload.utils import upload_to_func


class Upload(models.Model):

    BREAKFAST = '아침'
    LUNCH = '점심'
    DINNER = '저녁'

    MEALTIME_CHOICE = (
        (BREAKFAST, '아침'),
        (LUNCH, '점심'),
        (DINNER, '저녁'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upload_user', blank=True, null=True)
    image = models.ImageField(upload_to=upload_to_func, null=False, max_length=200)
    created_at = models.DateField(auto_now_add=True, null=True)
    mealtimes = models.CharField(choices=MEALTIME_CHOICE, max_length=20)

    def __str__(self):
        return f'{self.user, self.created_at, self.mealtimes, self.image}'

    class Meta:
        db_table = 'user_upload_info'


class FoodBio(models.Model):
    food_nm = models.CharField(max_length=100)  # Field name made lowercase.
    cal = models.FloatField(blank=True, null=True)  # Field name made lowercase.
    carb = models.FloatField(blank=True, null=True)  # Field name made lowercase.
    prot = models.FloatField(blank=True, null=True)  # Field name made lowercase.
    fat = models.FloatField(blank=True, null=True)  # Field name made lowercase.
    sodium = models.FloatField(blank=True, null=True)  # Field name made lowercase.
    amt_serve = models.FloatField(blank=True, null=True)  # Field name made lowercase.
    update_dt = models.DateTimeField(auto_now=True)  # Field name made lowercase.

    def __str__(self):
        return f'{self.food_nm}'

    class Meta:
        db_table = 'food_bio'


class UploadResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    upload_id = models.ForeignKey(Upload, db_column="upload_id", on_delete=models.CASCADE)
    food_code = models.ForeignKey(FoodBio, db_column='food_id', on_delete=models.CASCADE, max_length=20),
    carb_rate = models.FloatField(blank=True, null=True)
    prot_rate = models.FloatField(blank=True, null=True)
    fat_rate = models.FloatField(blank=True, null=True)
    sodium_rate = models.FloatField(blank=True, null=True)
    total_cal = models.FloatField(blank=True, null=True)
    create_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.user_id, self.user.n_code, self.food_code, self.total_cal}'

    class Meta:
        db_table = 'upload_result'
