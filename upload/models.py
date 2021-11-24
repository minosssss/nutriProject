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
        return f'{self.user.user_id, self.user.n_code, self.created_at, self.mealtimes, self.image}'

    class Meta:
        db_table = 'user_upload_info'

